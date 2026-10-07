# Python_Clean_Prepare_Data_Course/solutions.py

"""Worked final-project solution with observation provenance and a quality audit."""

# Reuse taught operations so each processing decision remains easy to inspect.
import numpy as np
import pandas as pd

from additional_lessons import time_mad_outliers
from Python_Clean_Prepare_Data_Course import (
    add_normalizations,
    create_light_curve,
    interpolate_small_gaps,
    polynomial_detrend,
    standardize_missing,
    time_window_smooth,
)


def prepare_data(data, sentinels=(-999,), event_intervals=((1.80, 2.20), (3.98, 4.32)), max_gap=5):
    """Return a prepared copy and audit for time_days and brightness observations.

    Time is in days and brightness in relative units. Require unique, increasing,
    finite timestamps and numeric finite-or-missing brightness. Event intervals
    mark regions excluded from a cubic baseline fit. max_gap counts missing rows,
    rather than elapsed days. No files are written and input data stays unchanged.
    Centered preprocessing is intended for retrospective analysis.
    """
    times = data["time_days"]
    values = data["brightness"]
    if not np.isfinite(times).all() or not times.is_unique or not times.is_monotonic_increasing:
        raise ValueError("Time must be finite, unique, and increasing.")
    if np.isinf(values).any():
        raise ValueError("Document and standardize infinite measurements first.")
    if not isinstance(max_gap, int) or max_gap < 0:
        raise ValueError("max_gap must be a nonnegative integer.")

    # Preserve observations and flags so estimated values remain distinguishable.
    prepared = standardize_missing(data, "brightness", sentinels)
    prepared["brightness_raw"] = values
    prepared["was_missing"] = prepared["brightness"].isna()
    prepared["was_outlier"] = time_mad_outliers(prepared, "brightness")
    prepared.loc[prepared["was_outlier"], "brightness"] = np.nan
    before_fill = prepared["brightness"].isna()
    prepared = interpolate_small_gaps(prepared, "brightness", limit=max_gap)
    prepared["was_interpolated"] = before_fill & prepared["brightness"].notna()
    prepared = prepared.rename(columns={"brightness": "brightness_clean"})
    prepared = add_normalizations(prepared, "brightness_clean")

    # Exclude interpolated samples as well as transit regions from baseline fitting.
    baseline = ~prepared["was_interpolated"]
    for start, stop in event_intervals:
        baseline &= ~times.between(start, stop)
    if (baseline & prepared["brightness_clean"].notna()).sum() < 4:
        raise ValueError("A cubic baseline needs at least four eligible observations.")
    prepared = polynomial_detrend(prepared, "relative_brightness", degree=3, mask=baseline)
    prepared["smoothed"] = time_window_smooth(prepared, "detrended", 0.05, 0.05)
    prepared["trailing_median"] = time_window_smooth(prepared, "detrended", 0.10, 0, "median")
    audit = pd.DataFrame({
        "check": ["input_rows", "sentinels_replaced", "outliers_flagged", "values_interpolated", "missing_remaining"],
        "value": [len(data), int(values.isin(sentinels).sum()), int(prepared["was_outlier"].sum()),
                  int(prepared["was_interpolated"].sum()), int(prepared["brightness_clean"].isna().sum())],
    })
    return prepared, audit


# Show the final project on a new noise realization without writing output files.
if __name__ == "__main__":
    result, quality = prepare_data(create_light_curve(seed=7))
    print(quality.to_string(index=False))
    print(result.head().to_string(index=False))
