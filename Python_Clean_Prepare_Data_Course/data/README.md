# Practice data provenance

CSVs were exported with `scipy.io.loadmat` from the supplied MAT files.
Original numeric values and missingness are preserved. Empty CSV fields
represent NaN and pandas reads them back as NaN.

| CSV | Source arrays | Shape and coordinates |
|---|---|---|
| `population.csv` | `populationData.mat`: `yr`, `population` | 33 rows; years 1950–2014 at two-year intervals |
| `gas_prices.csv` | `gaspriceData.mat`: `yrRaw`, `pricesRaw` | 19 rows; years 1990–2008; 10 series |
| `electricity.csv` | `electricityData.mat`: `usage`, `total` | 315 rows; 4 usage series, total and zero-based sample index |

The population exercise treats zero as missing. This assumption is specific
to the exercise; zero is valid in many other datasets.

Country and sector string objects and electricity datetime objects are opaque
to the simple SciPy reader. `price_01`–`price_10` and `usage_01`–`usage_04`
identify array positions, not decoded countries or sectors. The electricity
`sample_index` is a row coordinate, not a date. The fourth usage column is
numerically identical to the supplied total; both preserve the source structure.

Units and calendar metadata are not established by the readable arrays.
Obtain verified metadata before interpreting physical units or calculating
usage per day. CSVs are included in Git so Python examples do not depend on
ignored MAT files.
