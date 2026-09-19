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

The cleaning steps run in order. If the final validation fails, the cleaned
file is not exported. 

### 2. Required Questions

The questions are calculated by `question.py` using the cleaned data.

| Step | Process |
|---:|---|
| 1 | Load `worldData_cleaned.csv` |
| 2 | Check that each ISO code is unique |
| 3 | Count countries or areas in each continent and find the highest count |
| 4 | Calculate the combined area of each UN region and find the largest |
| 5 | Rank countries or areas by life expectancy and select the highest |
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



### Quick Start
### Requirements

Before running the project, make sure Python 3.10 or later is installed.

The main Python packages used are:

- pandas;
- Streamlit;
- pytest.

### 1. Download the Project

Clone the GitHub repository:

```bash
git clone https://github.com/lucas2052/codeChallange_worldbank.git
```

Move into the project folder:

```bash
cd codeChallange_worldbank
```

Alternatively, download the repository as a ZIP file from GitHub and open
the extracted folder in a terminal.

### 2. Create a Virtual Environment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Using a virtual environment is recommended but not required.

### 3. Install the Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Complete Project

```bash
python run.py
```

This command:

1. cleans and validates `worldData.csv`;
2. creates or replaces `worldData_cleaned.csv`;
3. prints the answers to the required questions in the terminal;
4. starts the local interactive interface.

The interface should open automatically in the default browser. If it does
not open, use the local URL shown in the terminal, usually:

```text
http://localhost:8501
```







### Data Define










### Key Challenges and Decisions

#### Handling `NA`

During a hand-made check, I found that pandas treated `NA` as a missing
value. However, `NA` is the ISO code for Namibia.

So I updated the CSV loading settings to keep `NA` as text. Then the actual missing
values, including `#N/A` and empty text, are marked in a separate cleaning
step.

#### Defining Numeric Ranges

The first numeric range checks only removed zero or negative values. During
manual review, I found that Haiti had a population value of approximately
`1.06`. 

Although this value was not empty or negative, it was not reasonable for a
country-level population field. I reviewed 2014 country-level reference data
and updated the accepted ranges for related metrics in order to make sure the range setting close with reality.

#### Testing Boundary Cases

The dataset contains several types of data quality problems, so testing only
normal values was not enough.

The unit tests include both normal and boundary cases, such as:

- missing and empty values;
- completely duplicated and conflicting records;
- duplicated columns;
- invalid ISO code formats;
- values out of the accepted numeric ranges;
- filter combinations that return no records;

### Limitation
