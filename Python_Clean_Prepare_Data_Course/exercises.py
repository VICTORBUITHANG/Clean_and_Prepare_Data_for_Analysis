# Python_Clean_Prepare_Data_Course/exercises.py

"""Practice prompts without solutions; use solutions.py after attempting them.

Work in the notebook or a separate file. No code runs on import. Use the course
CSV inputs and documented units; explain the assumptions behind each result.
"""

# Each exercise corresponds to a preprocessing decision in the MATLAB course.
EXERCISES = [
    "1. In [2, NaN, 5, 3, NaN], count missing values and compare mean, nanmean, and zero replacement.",
    "2. Standardize NaN and -999 in [2, NaN, 5, 3, -999, 4]. Keep zero as a valid observation.",
    "3. Flag light-curve outliers with a 0.5-day median/MAD window at thresholds 3, 5, and 8. Plot flags before replacing values.",
    "4. Interpolate y=[0, NaN, 7, 8, NaN, 2, -3, NaN, -8] at x=[0, 2, 3, 4, 7, 9, 10, 12, 15]. Compare nearest, linear, spline, and pchip.",
    "5. In population.csv, treat zero as missing for this exercise. Compare linear and PCHIP estimates; preserve measured values.",
    "6. In gas_prices.csv, count missing values per series, remove incomplete rows, and calculate columnwise sample z scores.",
    "7. In electricity.csv, center each column, scale by its first observation, and map it to [-1, 1]. Do not invent sector names or dates.",
    "8. Fit a cubic light-curve baseline outside the supplied transit intervals. Recover the trend by subtracting residuals from the normalized data.",
    "9. Compare 3-point and 17-point moving means and trailing/leading 4-point medians. Explain window width and use of future data.",
    "10. Build prepare_data returning prepared observations and an audit. Retain original values, outlier and interpolation flags, and long gaps. Run with seed=7.",
]


def show_exercises():
    """Print the ten prompts in order; no inputs or file side effects."""
    for exercise in EXERCISES:
        print(exercise, "\n")


# Display prompts when learners run this file directly.
if __name__ == "__main__":
    show_exercises()

