# Clean and Prepare Data for Analysis with Python

A self-paced Python adaptation of the MATLAB course in the parent folder.
Allow **60–90 minutes** for the guided course and **30–45 minutes** for additional
activities. Prerequisites: Python indexing, functions, arrays and basic plotting.

## Start studying

Use `/Users/victorbui/venvs/ai312`. From the project root:

```bash
/Users/victorbui/venvs/ai312/bin/python -m jupyter lab Python_Clean_Prepare_Data_Course/Python_Clean_Prepare_Data_Course.ipynb
```

Select a kernel using that environment. If it is not listed, register it:

```bash
/Users/victorbui/venvs/ai312/bin/python -m ipykernel install --user --name ai312 --display-name "Python ai312"
```

Read each explanation, attempt its practice cell, then inspect the following
solution. `exercises.py` provides ten independent prompts. The editable
`Python_Clean_Prepare_Data_Study_Guide.docx` is the current study guide;
previous PDF and LaTeX materials remain locally.

## Course sequence

| MATLAB module | Python activity |
|---|---|
| Introduction | Inspect a simulated light curve and its documented defects |
| Remove Outliers | Compare local median/MAD thresholds and window definitions |
| Work with Missing Data | Locate NaN, standardize sentinels, ignore, delete, replace |
| Interpolate Missing Data | Nearest, linear, spline, PCHIP, irregular coordinates, gap limits |
| Shift and Scale Data | Center, z-score, first observation, range and relative scaling |
| Remove Unwanted Trends | Fit a cubic baseline while excluding transit regions |
| Smooth Noisy Data | Mean versus median, 3 versus 17 samples, leading and trailing windows |
| Conclusion | Build a reusable pipeline, preserve provenance, validate and export |

The notebook includes worked examples, practice cells, solutions and inline
checks. Additional activities use CSV exports of the supplied MATLAB data.

## Run the examples

From the project root:

```bash
/Users/victorbui/venvs/ai312/bin/python Python_Clean_Prepare_Data_Course/Python_Clean_Prepare_Data_Course.py
/Users/victorbui/venvs/ai312/bin/python Python_Clean_Prepare_Data_Course/additional_lessons.py
/Users/victorbui/venvs/ai312/bin/python Python_Clean_Prepare_Data_Course/exercises.py
/Users/victorbui/venvs/ai312/bin/python Python_Clean_Prepare_Data_Course/solutions.py
```

The main script writes prepared data, an audit and two figures to `output/`,
overwriting the same named files on repeat runs. Other scripts print activities
or return tables without writing files. The final-project solution retains raw
observations and missing, outlier and interpolation flags and excludes estimated
values from its baseline fit.

## Data and method conventions

- The light curve is simulated, not an actual Kepler observation. Kepler and
  sensor files referenced in the source were not supplied.
- CSVs in `data/` retain the readable numeric MATLAB arrays. See
  [data provenance](data/README.md) for labels and limitations.
- The main examples use population z scores (`ddof=0`). Use `ddof=1` to match
  MATLAB default sample-standard-deviation z scores.
- The main rolling detector uses sample-count neighborhoods and a two-stage
  rolling deviation estimate. `time_mad_outliers` computes a true local MAD in
  a centered 0.5-day window. Review flagged points; counts can differ.
- Gap limits count complete missing runs in rows. Five irregular samples can
  span different durations; add an elapsed-time rule for real measurements.
- Smoothing skips missing neighbors and retains missing output timestamps.
  Centered filtering and baseline fitting use future information; the whole
  workflow is retrospective.
- For predictive modeling, fit scaling and imputation parameters on training
  observations only.

## Dependencies and Git

`requirements.txt` records installed numerical package versions and Jupyter
requirements. For another Python 3.12 environment, use its executable with
`-m pip install -r Python_Clean_Prepare_Data_Course/requirements.txt`.

Git is initialized in the parent folder. Python source, the unexecuted notebook,
READMEs, requirements and CSV practice inputs are eligible for tracking.
Documents, MAT files, generated outputs, caches and logs are ignored.
No commit, push or remote configuration is performed during course creation.
