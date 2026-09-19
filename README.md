# World Data Challenge

## Summary

This project cleans and analyses the provided `worldData.csv` dataset.
The cleaned results are presented in a local interactive interface, allowing
users to explore the data without writing code.

The project uses:

- **Python** as the main programming language;
- **pandas** to load, clean, validate, and analyse the data;
- **Streamlit** to build the interactive interface;
- **pytest** to test the main functions.

The project can:

- remove missing, duplicated, and invalid records;
- validate the final data before exporting it;
- export the cleaned data as a CSV file;
- answer the four questions included in the challenge;
- filter the data using one or more conditions;
- display summary statistics and filtered records;
- test the cleaning, analysis, and interface logic.


## Interface

The interface allows users to:

- select one or more continents, regions, subregions, and country or area types;
- update the results automatically when a filter changes;
- view summary statistics cards;
- see the highest and lowest value and its country or area;
- see how many records are below the average for each numeric field;
- view the matching records in an interactive table;
- sort the table by different columns;
- open the table in full-screen mode;
- download the filtered table to local device;
- warning if the result is empty;

![World Data interface](images/interface.png)


## Project Structure

```text
WorldDataChallenge/
├── README.md
├── requirements.txt
├── run.py
├── cleandata.py
├── question.py
├── interface.py
├── worldData.csv
├── worldData_cleaned.csv
├── images/
│   └── interface.png
└── tests/
    ├── test_cleaned_data.py
    ├── test_questions.py
    └── test_interface.py
```

- `run.py` runs the cleaning, analysis, and interface stages in order.
- `cleandata.py` cleans, validates, and exports the original data.
- `question.py` calculates the answers to the required questions.
- `interface.py` provides the local interactive interface.
- `worldData.csv` is the original data provided for the challenge.
- `worldData_cleaned.csv` is the cleaned data created by `cleandata.py`.
- `requirements.txt` lists the required packages.
- `tests/` contains the tests for the cleaning, analysis, and interface logic.
- `images/` contains the interface image used in this README.


## Approach

The project follows seven main stages:

1. **Review** — inspect the original data structure and other basica informations.
2. **Prepare** — remove spaces around text and define missing values and mark them.
3. **Clean** — remove missing records, duplicated values, and columns that are not included in the requirement.
4. **Standardise** — convert numeric columns to the required types, define accepted numeric ranges, and remove invalid records.
5. **Validate and export** — check the final columns, data types, ISO codes, duplicates, and numeric ranges before saving.
6. **Analyse** — group the cleaned data by continent, region, and subregion, then calculate counts, totals, averages, and the required highest or lowest results.
7. **Present** — create filter options from the cleaned data, apply individual or combined selections, calculate summary statistics for the filtered subset, and display the results in consistent summary cards and an interactive table.


## Process
### 1. Data Cleaning

The cleaning process is managed by `cleandata.py`.

| Step | Process |
|---:|---|
| 1 | Load the original CSV file and inspect its basic information |
| 2 | Keep `NA` as Namibia's ISO code |
| 3 | Remove spaces around text and mark empty text and `#N/A` as missing |
| 4 | Find and remove rows containing missing values |
| 5 | Find and remove repeated columns, duplicated rows, and the old CSV index |
| 6 | Round numeric values and convert the required columns to integers |
| 7 | Define accepted numeric ranges using reviewed 2014 reference data |
| 8 | Find and remove records containing invalid numeric values |
| 9 | Check whether each `iso_a2` code is unique |
| 10 | Validate the final columns, missing values, duplicates, text, ISO codes, numeric types, and ranges |
| 11 | Display the final data size and export `worldData_cleaned.csv` |


### 2. Required Questions

The questions are calculated by `question.py` using the cleaned data.

| Step | Process |
|---:|---|
| 1 | Load `worldData_cleaned.csv` |
| 2 | Check that each ISO code is unique |
| 3 | Count countries or areas in each continent and find the highest count |
| 4 | Calculate the combined area of each UN region and find the largest |
| 5 | Rank countries by life expectancy and select the highest |
| 6 | Calculate the average GDP per capita for each subregion |
| 7 | Find the subregions with the highest and lowest average GDP per capita |

### 3. Interactive Interface

The interface is provided by `interface.py`.

| Step | Process |
|---:|---|
| 1 | Load the cleaned data |
| 2 | Create filter options from the available values |
| 3 | Allow users to filter by continent, region, subregion, and type |
| 4 | Combine selected filters using AND logic |
| 5 | Handle cases where no filter is selected or no record matches |
| 6 | Calculate summary statistics for the filtered results |
| 7 | Display the average, highest, lowest, and below-average count |
| 8 | Display the filtered records in an interactive table |


## Quick Start

Python 3.10 or later is recommended.

### 1. Download the Project

Clone the repository and move into the project folder:

```bash
git clone https://github.com/lucas2052/codeChallange_worldbank.git
cd codeChallange_worldbank
```

### 2. Install the Required Packages

```bash
python -m pip install -r requirements.txt
```

### 3. Run the Complete Project

```bash
python run.py
```

This command:

1. cleans and validates the original data;
2. creates or replaces `worldData_cleaned.csv`;
3. prints the answers to the required questions;
4. starts the local interactive interface.

Press `Control + C` to stop the interface.

### 4. Run the Tests

After stopping the interface, run:

```bash
python -m pytest -v
```

Pytest will find and run all test files in the `tests/` folder.



## Data Definitions
### Cleaning Rules

| Data issue | Definition | Action |
|---|---|---|
| Missing values | Empty text, `#N/A`, or a pandas missing value. `NA` is excluded because it is Namibia's ISO code | Remove the complete row |
| ISO code format | The code must contain two uppercase letters and appear only once | Stop validation if an invalid or repeated code remains |
| Duplicates | Completely repeated rows or columns containing the same values | Keep the first copy and remove the repeated copy |
| Unexpected data type | The six descriptive columns must contain text. `area_km2`, `pop`, `lifeExp`, and `gdpPercap` are stored as integers | Convert text columns to strings, round valid numeric values, and convert them to integers. Stop and warning if a numeric value cannot be converted |
| Invalid numeric range | A numeric value is below or above the accepted limits selected from reviewed 2014 reference data | Remove the complete row |
| Unneeded columns | Columns that are not part of the required output, such as the old CSV index | Remove the column |


### Accepted Numeric Ranges

| Column | Minimum | Maximum | Unit |
|---|---:|---:|---|
| `area_km2` | 1 | 17,100,000 | Square kilometres |
| `pop` | 800 | 1,400,000,000 | People |
| `lifeExp` | 40 | 86 | Years |
| `gdpPercap` | 200 | 200,000 | Current US dollars per person |

These ranges were selected after reviewing unexpected values and comparing
them with published 2014 reference data. 

### Interface Summary Statistics
The summary is calculated separately for:

- area;
- population;
- life expectancy;
- GDP per capita.

| Summary item | Definition |
|---|---|
| Number of results | Number of unique `iso_a2` codes in the filtered data |
| Average | The sum of all values divided by the number of filtered records |
| Highest | Highest value and its related area |
| Lowest | Lowest value and its related area |
| Below average | Number of records with a value lower than the arithmetic mean |



## Key Challenges and Decisions
### Handling Edge Cases

The initial cleaning rules could not identify every unusual case. Manual
review found that `NA` was Namibia's valid ISO code and that Haiti's
population value was positive but still unreasonable.

I added specific loading and numeric range rules to handle these cases.
A more reliable solution would compare ISO codes and country indicators with
maintained authoritative reference data.

### Extending the Tests

I first wrote unit tests using normal input to check that each function worked.
After finding unusual values in the dataset, I extended the tests to include
invalid and boundary cases.

These tests check values at and outside the accepted numeric limits, repeated
ISO codes, missing values, and filter combinations with no results. This
helped confirm that the cleaning and interface rules worked as intended.

## Limitation
- **Limited reusability** — the program is closely tied to the structure of
  `worldData.csv`. Using the program with a different CSV structure would require manual changes to the cleaning functions and tests.

- **External validation** — The program does not compare each record with
  an authoritative external source, so it checks data plausibility rather
  than factual accuracy.

- **Possible selection bias** — rows containing missing or invalid values are
  removed completely.Their removal may affect the final statistics.

- **Numeric precision** — decimal values are rounded and stored as integers. 
  This causes some precision to be lost.


## Possible Improvements
- **Reusable rules** — store column names, data types, missing-value rules,
  and numeric ranges in a configuration file. This would make it easier to
  use the program with other CSV files.

- **Official reference checks** — compare ISO codes and country values with
  reliable official sources instead of using only format and range checks.

- **Review removed records** — save removed records and their removal reasons
  in a separate file. They can then be checked before they are corrected or
  permanently removed.