# World Data Challenge

## Summary
This project cleans and analyses the `worldData.csv` dataset, which is
based on the `worldData` dataset provided.

The original dataset contained 189 rows and 12 columns. After removing
missing, duplicated, and invalid records, the cleaned dataset contained
143 rows and 10 columns.

The project uses Python, pandas, Streamlit, and pytest to:

- clean and validate the original country data;
- answer the four questions included in the challenge;
- filter data by continent, region, subregion, and country type;
- display summary statistics for area, population, life expectancy, and GDP per capita;
- allow users to view and download the filtered data;
- test the main cleaning, caculate, and interface functions.


## Interface Preview
![World Data interface](images/interface.png)

## Project Structure


## Approach
The data cleaning process follows the steps below:

```mermaid
flowchart TD
    A[Set the input and output paths] --> B[Load worldData.csv]
    B --> C[Keep NA as Namibia's ISO code]
    C --> D[Inspect shape, columns, types, and statistics]

    D --> E[Remove spaces around text]
    E --> F[Change empty text and #N/A to missing values]
    F --> G[Find and report rows with missing values]
    G --> H[Remove rows with missing values]

    H --> I[Find columns containing the same values]
    I --> J[Remove repeated columns and keep the first]
    J --> K[Remove the old CSV index column]

    K --> L[Find and report completely duplicated rows]
    L --> M[Remove completely duplicated rows]

    M --> N[Convert numeric columns to integers]
    N --> O[Round decimal values before conversion]

    O --> P[Define accepted numeric ranges]
    P --> Q[Find and report invalid numeric rows]
    Q --> R[Remove invalid numeric rows]

    R --> S[Check for repeated ISO codes]
    S --> T{Do repeated ISO codes remain?}

    T -- Yes --> U[Stop and report a validation error]
    T -- No --> V[Run final validation]

    V --> W[Check final columns]
    W --> X[Check missing and duplicated records]
    X --> Y[Check text and ISO code formats]
    Y --> Z[Check integer types and numeric ranges]

    Z --> AA[Display the final data information]
    AA --> AB[Export worldData_cleaned.csv]
```

The cleaning process first reports each data quality issue before removing
the affected records. The final validation must pass before the cleaned
data is exported.

## Main Results

### 1. Data Cleaning

### 2. Required Questions

### 3. Interactive Interface