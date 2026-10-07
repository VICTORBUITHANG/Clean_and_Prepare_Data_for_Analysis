# Python_Clean_Prepare_Data_Course/additional_lessons.py

"""Companion activities matching the MATLAB examples and supplied numeric data.

Run directly to print comparisons. Import functions into the notebook to try
different methods. All CSV paths are resolved relative to this file.
"""

# Import interpolation tools and the table libraries used in the lessons.
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline, PchipInterpolator, interp1d

DATA_DIR = Path(__file__).resolve().parent / "data"


def interpolate_internal(x, y, method="linear"):
    """Return estimates at internal missing samples using actual coordinates.

    x must be finite, strictly increasing, and aligned with numeric y. Supported
    methods are nearest, linear, spline, and pchip. Boundary gaps stay missing;
    the caller must decide whether the duration of an internal gap is acceptable.
    No files are written and input arrays are not modified.
    """
    locations = np.asarray(x, dtype=float)
    values = np.asarray(y, dtype=float)
    if locations.ndim != 1 or values.shape != locations.shape:
        raise ValueError("x and y must be aligned one-dimensional arrays.")
    if not np.isfinite(locations).all() or not (np.diff(locations) > 0).all():
        raise ValueError("x must be finite and strictly increasing.")
    valid = np.isfinite(values)
    if valid.sum() < 2:
        raise ValueError("Interpolation needs at least two finite observations.")
    # Disable extrapolation so unknown behavior outside observations stays visible.
    known_x, known_y = locations[valid], values[valid]
    if method in {"nearest", "linear"}:
        model = interp1d(known_x, known_y, kind=method, bounds_error=False,
                         fill_value=np.nan)
    elif method == "spline":
        model = CubicSpline(known_x, known_y, extrapolate=False)
    elif method == "pchip":
        model = PchipInterpolator(known_x, known_y, extrapolate=False)
    else:
        raise ValueError("Choose nearest, linear, spline, or pchip.")
    result = values.copy()
    result[~valid] = model(locations[~valid])
    return result


def time_mad_outliers(data, column, window_days=0.5, threshold=5):
    """Flag deviations from a local median using a window measured in days.

    data contains time_days and a numeric measurement column. Each centered
    neighborhood uses its own median and MAD; 1.4826 scales MAD for normal noise.
    Missing samples and windows with fewer than nine finite observations are
    not flagged. Zero MAD is left unclassified for manual review. This explicit
    teaching implementation is quadratic and is intended for small course data.
    """
    if window_days <= 0 or threshold <= 0:
        raise ValueError("window_days and threshold must be positive.")
    times = data["time_days"].to_numpy(dtype=float)
    values = data[column].to_numpy(dtype=float)
    flags = np.zeros(len(values), dtype=bool)
    # Compute deviations from the same median within each physical-time window.
    for position, current_time in enumerate(times):
        local = values[np.abs(times - current_time) <= window_days / 2]
        local = local[np.isfinite(local)]
        if local.size < 9 or not np.isfinite(values[position]):
            continue
        center = np.median(local)
        scale = 1.4826 * np.median(np.abs(local - center))
        if scale > 0:
            flags[position] = abs(values[position] - center) > threshold * scale
    return pd.Series(flags, index=data.index, name="outlier")


def run_additional_lessons():
    """Print worked comparisons and return tables for interactive exploration.

    Uses checked-in CSV exports of the local MAT numeric arrays. Generic column
    labels are deliberate because MATLAB string metadata is not decoded. This
    activity does not write files or infer calendar dates, countries, or units.
    """
    # Missing-data semantics differ between NumPy's mean and pandas' mean.
    small = np.array([2, np.nan, 5, 3, np.nan])
    print("Ordinary NumPy mean:", np.mean(small))
    print("NumPy mean ignoring NaN:", np.nanmean(small))
    print("Missing count:", np.isnan(small).sum())
    print("Mean after replacement with zero:", np.nan_to_num(small, nan=0).mean())

    # Reproduce the irregular locations in the MATLAB interpolation activity.
    x = np.array([0, 2, 3, 4, 7, 9, 10, 12, 15], dtype=float)
    y = np.array([0, np.nan, 7, 8, np.nan, 2, -3, np.nan, -8])
    comparison = pd.DataFrame({"x": x, "observed": y})
    comparison["by_position"] = pd.Series(y).interpolate()
    for method in ("nearest", "linear", "spline", "pchip"):
        comparison[method] = interpolate_internal(x, y, method)
    print("\nInterpolation methods\n", comparison.to_string(index=False))

    # Population zeros are treated as missing only for this supplied exercise.
    population = pd.read_csv(DATA_DIR / "population.csv")
    population["observed_population"] = population["population"].replace(0, np.nan)
    for method in ("linear", "pchip"):
        population[method] = interpolate_internal(
            population["year"], population["observed_population"], method
        )
    print("\nPopulation interpolation\n", population.head(10).to_string(index=False))

    # Retain complete rows and compare missingness before making a replacement.
    gas = pd.read_csv(DATA_DIR / "gas_prices.csv").set_index("year")
    print("\nGas-price missing values per series\n", gas.isna().sum())
    print("Complete gas-price rows:", len(gas.dropna()))
    gas_z = (gas - gas.mean()) / gas.std(ddof=1)
    print("Sample-standard-deviation z scores\n", gas_z.head())

    # Divide by the actual first row, not the first nonmissing row.
    usage = pd.read_csv(DATA_DIR / "electricity.csv").set_index("sample_index")
    first = usage.iloc[0]
    if (first == 0).any() or first.isna().any():
        raise ValueError("First-observation scaling needs nonzero finite values.")
    first_scaled = usage / first
    print("\nElectricity ratios to first observation\n", first_scaled.head())

    # A trailing four-point window contains this point and three previous points.
    signal = pd.Series(np.sin(np.arange(0, 6.01, 0.2)))
    windows = pd.DataFrame({"signal": signal})
    windows["trailing4"] = signal.rolling(4, min_periods=1).median()
    windows["leading4"] = signal.iloc[::-1].rolling(4, min_periods=1).median().iloc[::-1]
    print("\nTrailing and leading medians\n", windows.head())
    return comparison, population, gas_z, first_scaled, windows


# Direct execution runs the companion activities without changing course inputs.
if __name__ == "__main__":
    run_additional_lessons()

