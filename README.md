<div align="center">
  <img src="asset/asset-01.png" alt="Deskripsi Gambar" width="2600">
</div>

---
<div align = 'justify'>

  # 1. Introducing `workbench`
  `workbench` is my personal open-source toolkit built to automate, streamline, and eliminate repetitive `country-base` data cleaning activities within economic and financial data mining pipelines. The core goal of `workbench` is to serve as an end-to-end data harmonization engine, enabling seamless integration of multi-source macro-financial datasets into a unified, clean, and model-ready structure with minimal manual intervention.

  It provides a versatile framework designed to tackle specific challenges, such as:
  1. When you want to analyze data coming from various sources with different structures and schemas.
  2. When your data comes from various sources with sample frequency disparities, forcing you to waste time standardizing frequencies first.
  3. When standardized data contains random `NaN` values or inconsistent missing value representations across instances that require further tidying up.
  4. Resolving entity resolution and naming inconsistencies (e.g., "USA", "United States", "US") across different international organization standards (IMF, OECD, Scimago) by mapping them directly to a standardized ISO3 code (`ISO 3166-1 alpha-3`).
  5. Handling non-standard missing value representations (such as `'..'`, `' '`, or provider-specific placeholders) across multiple datasets and centralizing them into a single, clean `NaN` standard before feature engineering.
  6. Aligning disparate feature schemas across multi-source datasets without manual column matching, index matching, or repeated renaming iterations.
  7. Structuring cross-country panel data into a unified geographic universe based on a master ISO list (`_iso_master`), ensuring consistent cross-sectional alignment for downstream econometric modeling.

# 2. Supported Data Sources & Compatibility on `workbench`

  Before diving into the code, let's talk about the data compatible with `workbench`. Here’s a list of primary datasets from global institutions that you can easily process without worrying about formatting headaches:

  | Institution | Dataset | Covering How Many Data Feature | Example Feature |
  | :--- | :--- | :--- | :--- |
  | **IMF** | IFS - Quarterly Government Finance (QGFS) | 3 Features / Variables | - Statement of Sources and Uses of Cash<br>- Balance Sheet Account<br>- Statement of Operations |
  | **IMF** | International Investment Position (IIP) | 119 Features / Variables | - Derivatives, Portfolio investment, Debt securities, Non-financial corporations<br>- Direct investment between fellow enterprises, Debt instruments|
  | **IMF** | World Economic Outlook (WEO) | Multi-Variable Macro Series | - Real GDP growth (%)<br>- Inflation, average consumer prices<br>- Current account balance (% of GDP) |
  | **IMF** | Coordinated Direct Investment Survey (CDIS) | Cross-Border Investment Features | - Inward direct investment positions<br>- Outward direct investment positions by counterpart economy |
  | **World Bank** | World Development Indicator | 1498 Features / Variables | - Bank capital to assets ratio (%)<br>- Domestic credit to private sector by banks (% of GDP)<br>- Commercial bank branches (per 100,000 adults) |
  | **World Bank** | Education Datasets | 8450 Features / Variables | - Labor force with advanced education, male (% of male labor force)<br>- Labor force with basic education (% of total labor force) |
  | **World Bank** | Health Nutrition & Population | 475 Features / Variables | - Public spending on education, total (% of GDP)<br>- Risk of catastrophic expenditure for surgical care |
  | **ADB** | Key Indicators for Asia and the Pacific | 100+ Regional Indicators | - Regional poverty rates<br>- Trade and balance of payments for Asian economies<br>- Infrastructure and digital connectivity metrics |

  And extensive datasets seamlessly supported across major global macroeconomic & financial data providers:
  * **More IMF Data**: Like Fuel Fossil Subsidies Data (IMF:FFS) and all IMF datasets.
  * **OECD Data Portal**: Structural analysis (STAN), tax revenue statistics, national accounts, environmental policy stringency metrics, and many more.
  * **Penn World Table (PWT)**: Purchasing power parity (PPP), real GDP per capita, total factor productivity (TFP), capital stock estimates, and many more.
  * **SCImago Journal & Country Rank**: Country-level scientific output, total citations, h-index, international research collaborations, and many more.
  * **BIS (Bank for International Settlements)**: Credit to the non-financial sector, locational banking statistics, effective exchange rate indices (EER), property prices and many more.
  * **UNCTAD (UN Trade & Development)**: Foreign direct investment (FDI) inflows/outflows, merchandise trade matrix, commodity price indices, and many more.
  * **Regional Development Banks (AfDB, IDB, EBRD)**: Regional economic integration, development project indicators, and fiscal sustainability metrics across Africa, Latin America, and Eastern Europe.
---

  # 3. Quickstart & Usage Tutorial `workbench.BaseUtility`

  Here is a step-by-step guide on how to leverage `BaseUtility` to harmonize, clean, and merge two datasets from completely different international sources into a single model-ready `DataFrame`.
  
### Step 1: Import Module & Initialize `BaseUtility`

The entry point of the `workbench` data pipeline begins by importing `BaseUtility` and instantiating it with two target raw datasets. `BaseUtility` natively handles dataset-specific formatting disparities, allowing you to parse distinct delimiters and decimal conventions simultaneously.

```python
from workbench import BaseUtility
```

#### Initialize BaseUtility with two raw CSV datasets
```python
utility = BaseUtility(
    first_path="data/sci-15.csv",
    second_path="data/oecd-sci-15.csv",
    delimiter=(",", ";"),
    decimal=(".", ",") 
)

```

#### Parameter Breakdown:

* **`first_path`** (`str`): File path to the primary dataset (`self.data0`).
* **`second_path`** (`str`): File path to the secondary dataset (`self.data1`).
* **`delimiter`** (`tuple` of `str`, *optional*): Column separation characters specified as `(delimiter_0, delimiter_1)`. Defaults to `None` (standard comma `,` for both).
* **`decimal`** (`tuple` of `str`, *optional*): Decimal point marks specified as `(decimal_0, decimal_1)`. Crucial when parsing datasets with European decimal formatting (e.g., `,`).


### Step 2: Standardize Column Names `BaseUtility.sanitize`

Before merging multi-source datasets, feature names must be standardized. The `sanitize` method renames specific columns in either the first or second dataset by mapping old column names to new, clean feature labels. 

Crucially, this step is used to rename the primary geographic entity column (e.g., `'Country'`, `'Country Name'`, or `'Nation'`) to `'iso3'`, which serves as the core key for downstream harmonization.

```python
utility.sanitize(
    which='first', 
    before=('Country', 'Math ', 'Science', 'Reading'), 
    after=('iso3', 'pisa_math', 'pisa_sci', 'pisa_read')
)

```

#### Parameter Breakdown:

* **`which`** (`str`): Specifies which dataset to sanitize. Accepts `'first'` (targets `self.data0`) or `'second'` (targets `self.data1`). Case-insensitive.
* **`before`** (`tuple` of `str`): A tuple containing the existing column names to be replaced.
* **`after`** (`tuple` of `str`): A tuple containing the new standardized column names corresponding to the order of `before`.

> **Note:** Always ensure that one of the sanitized output labels in `after` is named `'iso3'`. The `workbench` pipeline relies on `'iso3'` as the universal entity identifier in subsequent operations. 


### Step 3: Batch Rename Columns for the Second Dataset and sometimes `BaseUtility.popout`

After sanitizing the first dataset, apply the same standardization to the second dataset (`self.data1`). When you want to rename every column in the dataset at once without hardcoding individual original column names, you can dynamically pass a tuple of all existing columns into the `before` parameter. First, you can utilize `BaseUtility.popout` to remove certain variable/ feature that unnecessarily used. This case, `Documents`, that is total gross paper that accumulate between the citable and non-citable paper.

```python
utility.popout(
    which = 'second', 
    drop = ['Documents']
)
```
```python
utility.sanitize(
    which='second', 
    before=tuple(f for f in utility.data1.columns), 
    after=(
        'iso3', 
        'total_paper', 
        'tot_citable_paper',
        'tot_paper_cit', 
        'tot_paper_self_cit', 
        'h_index'
    )
)

```

#### Parameter Breakdown:

* **`which`** (`str`): Target dataset indicator set to `'second'` to perform changes on `self.data1`.
* **`before`** (`tuple` of `str`): A tuple containing target column names. In this case, `tuple([f for f in utility.data1.columns])` dynamically captures every existing column header in `data1`.
* **`after`** (`tuple` of `str`): A tuple of new feature names that maps 1-to-1 to the order of original columns extracted in `before`.

> **Pro Tip:** Using `tuple(utility.data1.columns)` is an efficient way to re-label all raw columns in one go, provided that your `after` tuple contains an identical number of items matching the exact order of the source columns.


### Step 4: Verify Column Renaming & Identify Cross-Dataset Disparities

Now that column names have been sanitized, inspect the first few rows and structural info of both DataFrames to verify the changes and assess the underlying data structure.

```python
print(utility.data0.head(3))
```
```console
        iso3   pisa_math    pisa_sci   pisa_read
0  Singapore  564.189681  555.574682  535.100157
1      Japan  532.439872  538.394751  515.958480
2    Estonia  519.529134  534.193746  519.142860
```
```python
print(utility.data1.head(3))
```
```console
             iso3  total_paper  tot_citable_paper  tot_paper_cit  tot_paper_self_cit  h_index
0   United States       578182           24586819        9265919               33.67     3388
1           China       454417           12017074        7053419               25.82     1595
2  United Kingdom       169439            7742844        1523076               35.88     2183

```

Next, inspect the DataFrame summary to examine total observation counts:

```python
print(utility.data0.info())
```
```console
<class 'pandas.DataFrame'>
RangeIndex: 70 entries, 0 to 69
Data columns (total 4 columns):
 #   Column     Non-Null Count  Dtype  
---  ------     --------------  -----  
 0   iso3       70 non-null     object 
 1   pisa_math  70 non-null     float64
 2   pisa_sci   70 non-null     float64
 3   pisa_read  70 non-null     float64
dtypes: float64(3), object(1)
memory usage: 2.3 KB
```
```python
print(utility.data1.info())
```
```console
<class 'pandas.DataFrame'>
RangeIndex: 231 entries, 0 to 230
Data columns (total 6 columns):
 #   Column              Non-Null Count  Dtype  
---  ------              --------------  -----  
 0   iso3                231 non-null    object 
 1   total_paper         231 non-null    int64  
 2   tot_citable_paper   231 non-null    int64  
 3   tot_paper_cit       231 non-null    int64  
 4   tot_paper_self_cit  231 non-null    float64
 5   h_index             231 non-null    int64  
dtypes: float64(1), int64(4), object(1)
memory usage: 11.0 KB

```

#### Key Takeaway!:

1. **Schema Alignment**: Both datasets successfully share the `iso3` column key, and feature names are clean and model-ready.
2. **Entity Name Inconsistency**: Although labeled as `iso3`, the values in both datasets still consist of raw country strings (e.g., `"Singapore"`, `"United States"`) rather than standardized 3-letter Alpha-3 ISO codes (e.g., `"SGP"`, `"USA"`).
3. **Observation Disparity / Sample Imbalance**: `data0` contains **70 observations** (covering OECD/PISA participating countries), whereas `data1` contains **231 observations** (covering global SCImago entities).

In standard `pandas` workflows, merging datasets with unequal observation counts and unstandardized entity names creates significant indexing conflicts, missing country alignment, and data loss. `workbench` resolves these exact structural hurdles in the `orchestrate` step.


### Step 5: Execute Master Harmonization & Cross-Sectional Orchestration `BaseUtility.orchestrate`

This step is the core engine of `workbench`. The `orchestrate` method solves both entity resolution issues and observation count disparities in a single operation. 

By passing provider-specific parameters, `workbench` maps raw country names (e.g., `"United States"`, `"Singapore"`) directly to standardized ISO3 codes (`ISO 3166-1 alpha-3`), aligns disparate sample sizes across a universal master geographic index (`_iso_master`), and standardizes missing value representations.

```python
# Harmonize country names to ISO3 codes and align both datasets across _iso_master
utility.orchestrate(
    special=('oecd', 'scimago'), 
    which_special=('first', 'second')
)

```

#### Parameter Breakdown:

* **`special`** (`tuple` of `str` or `str`): Specifies institutional cleaning rules to handle non-standard country naming conventions. Supported keywords include `'oecd'`, `'scimago'`, and `'imf'`.
* **`which_special`** (`tuple` of `str` or `str`): Indicates which dataset receives the corresponding rule in `special` (`'first'` for `data0`, `'second'` for `data1`).

---

#### What Happens Under the Hood?

When `orchestrate()` runs, `workbench` executes three automated transformations:

1. **Entity Resolution & ISO3 Standardization**:
* Dataset 1 (`'oecd'` mode): Maps country names (like `"Singapore"`, `"Estonia", "(B-S-J-G) China", "FYOMR (Former Yugoslavia)"`) to their official 3-letter codes (`"SGP"`, `"EST", "CHN", "MKD"`).
* Dataset 2 (`'scimago'` mode): Resolves entities (like `"United States"`, `"United Kingdom"`) into standardized codes (`"USA"`, `"GBR"`).


2. **Master Alignment across `_iso_master`**:
* Instead of discarding unmatched rows via conventional SQL-style joins, `workbench` re-indexes all extracted features against `_iso_master`, a comprehensive global list of ISO3 codes.
* Both the 70-country dataset (`data0`) and 231-country dataset (`data1`) are projected onto this identical geographic universe.


3. **Missing Value Normalization**:
* Non-standard provider placeholders (e.g., `' '`, `'..'`) or entities missing from one of the datasets are automatically filled with clean `'NaN'` strings, establishing uniform missing value representations across all columns.
* The result is stored directly inside `utility.masterdata` and the instances, until this steps is conducted, still to be `str`.


### Step 6: Inspect the Harmonized Master Dataset (`utility.masterdata`)

Following the execution of `orchestrate()`, both raw datasets are compiled into `utility.masterdata`. Print the first 30 rows of `masterdata` to inspect the unified cross-sectional structure.

```python

print(utility.masterdata.head(30))

```

```console
       pisa_math     pisa_sci    pisa_read total_paper tot_citable_paper tot_paper_cit tot_paper_self_cit h_index
ABW          NaN          NaN          NaN           8               420             1               28.0      35
AFG          NaN          NaN          NaN          76             17964           143             176.12      90
AGO          NaN          NaN          NaN          99              1484           180              13.74      75
AIA          NaN          NaN          NaN          12               211             2              16.23      32
ALA          NaN          NaN          NaN         NaN               NaN           NaN                NaN     NaN
ALB  413.1570218  427.2249831  405.2587603         474              8450           549              16.38     129
AND          NaN          NaN          NaN          22               670            19               26.8      50
ARE  427.4827368  436.7311447  433.5422869        4564            149492         11671              29.26     421
ARG  456.2955893  475.1865979  475.3323101       12449            360079         56011              25.95     646
ARM          NaN          NaN          NaN        1050             31581          5380              28.89     256
ASM          NaN          NaN          NaN           9               149             5               14.9      40
ATA          NaN          NaN          NaN         NaN               NaN           NaN                NaN     NaN
ATF          NaN          NaN          NaN         NaN               NaN           NaN                NaN     NaN
ATG          NaN          NaN          NaN          11               322             6              29.27      41
AUS  493.8962312  509.9938541  502.9005596       84762           3960638        646247               39.1    1584
AUT   496.742274  495.0374864  484.8655968       23269            968861         96330              36.71     998
AZE          NaN          NaN          NaN         804             25718          3018              30.62     182
BDI          NaN          NaN          NaN          51              1313            80              21.18      76
BEL  506.9843628   501.999714  498.5241897       30706           1430011        142203              40.89    1207
BEN          NaN          NaN          NaN         427             26186          1324              57.93     145
BES          NaN          NaN          NaN         NaN               NaN           NaN                NaN     NaN
BFA          NaN          NaN          NaN         542             15173          1667              26.57     163
BGD          NaN          NaN          NaN        3678            124667         16568              31.43     386
BGR  441.1899183  445.7719568  431.7175316        3940            113575         10152              26.56     394
BHR          NaN          NaN          NaN         365             24497           362              55.42     165
BHS          NaN          NaN          NaN          44              1284           121              24.23      83
BIH          NaN          NaN          NaN         935             19346          1381               19.4     173
BLM          NaN          NaN          NaN         NaN               NaN           NaN                NaN     NaN
BLR          NaN          NaN          NaN        1742             38054          6059              20.92     253
BLZ          NaN          NaN          NaN          31             18347            39             509.64      73

```

#### Key Takeaways from the Harmonized Output:

1. **Standardized Row Indexing**: The index is now comprised strictly of official 3-letter Alpha-3 ISO codes (`ABW`, `AFG`, `ALB`, `AUS`, `BEL`, etc.), replacing raw country strings completely.
2. **Unified Feature Alignment**: Indicators from Dataset 0 (`pisa_math`, `pisa_sci`, `pisa_read`) and Dataset 1 (`total_paper`, `tot_citable_paper`, `h_index`, etc.) are now merged side-by-side along the same row keys.
3. **Consistent Null Representation**: Entities present in SCImago but absent from PISA (e.g., Aruba - `ABW`, Afghanistan - `AFG`) display uniform `NaN` values for PISA features, maintaining complete structural integrity across all variables.

---

## 🚧 Work in Progress & Next Steps

> **Project Status Notice:**  
> The `workbench` toolkit is under active development! Source code refactoring, structural optimizations, and additional class methods/utilities are currently being built and tested.

More step-by-step tutorials, advanced feature alignment methods, and module deep-dives will be added as new updates drop. 

**Stay tuned & happy coding! See you in the next build!**

*Sincerely, Pasha, Muhammad*



</div>


