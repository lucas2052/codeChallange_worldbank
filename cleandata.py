from pathlib import Path
import pandas as pd


# 1. set the file paths
base_dir = Path(__file__).resolve().parent
input_path = base_dir / "worldData.csv"
output_path = base_dir / "worldData_cleaned.csv"


# 2. load the original data
# keep "NA" because it is the ISO code for Namibia
df = pd.read_csv(
    input_path,
    keep_default_na=False,
    na_values=["#N/A", ""]
)


# 3. view the original data
print("Original dataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData information:")
df.info()

print("\nSummary statistics:")
print(df.describe())


# 4. list the original text columns
raw_text_columns = (
    df.select_dtypes(
        include=["object", "string"]
    )
    .columns
    .tolist()
)

print("\nText columns:")
print(raw_text_columns)


# 5. clean the text columns
for column in raw_text_columns:
    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
    )


# 6. change empty text to missing values
df[raw_text_columns] = (
    df[raw_text_columns]
    .replace("", pd.NA)
)


# 7. check missing values
print("\nMissing values:")
print(df.isna().sum())

missing_rows = df[
    df.isna().any(axis=1)
]

print("\nRows with missing values:")
print(missing_rows)

print("\nNumber of rows with missing values:")
print(len(missing_rows))


# 8. remove rows with missing values
df = df.dropna().copy()

print("\nDataset shape after removing missing values:")
print(df.shape)


# 9. find duplicated rows
duplicate_rows = df[
    df.duplicated(keep=False)
]

print("\nDuplicated rows:")
print(duplicate_rows)

print("\nNumber of extra duplicated rows:")
print(df.duplicated().sum())


# 10. remove duplicated rows
df = df.drop_duplicates().copy()

print("\nDataset shape after removing duplicated rows:")
print(df.shape)


# 11. check if the two ISO columns are the repeated
iso_columns_are_equal = df["iso_a2"].equals(
    df["iso_a2.1"]
)

print("\nAre the two ISO columns the same?")
print(iso_columns_are_equal)

if not iso_columns_are_equal:
    raise ValueError(
        "iso_a2 and iso_a2.1 contain different values."
    )


# 12. remove columns that are not in the data description
df = df.drop(
    columns=[
        "Unnamed: 0",
        "iso_a2.1"
    ]
).copy()

print("\nColumns after removal:")
print(df.columns.tolist())


# 13. set the number columns
integer_columns = [
    "area_km2",
    "pop",
    "lifeExp",
    "gdpPercap"
]


# 14. change the number columns to integer
# Round the values before changing the type
for column in integer_columns:
    df[column] = (
        pd.to_numeric(
            df[column],
            errors="raise"
        )
        .round()
        .astype("int64")
    )


# 15. find values outside the properly defined ranges
invalid_area = (
    df["area_km2"] <= 0
)

invalid_population = (
    df["pop"] <= 0
)

invalid_life_exp = (
    (df["lifeExp"] <= 0)
    | (df["lifeExp"] > 100)
)

invalid_gdp = (
    df["gdpPercap"] <= 0
)


# 16. combine all incorrect range checks
incorrect_range_mask = (
    invalid_area
    | invalid_population
    | invalid_life_exp
    | invalid_gdp
)

print("\nIncorrect values found:")
print("Area:", invalid_area.sum())
print("Population:", invalid_population.sum())
print("Life expectancy:", invalid_life_exp.sum())
print("GDP per capita:", invalid_gdp.sum())


# 17. remove rows with incorrect values
df = df[
    ~incorrect_range_mask
].copy()

print("\nDataset shape after removing incorrect values:")
print(df.shape)


# 18. check the final data
print("\nFinal dataset shape:")
print(df.shape)

print("\nFinal columns:")
print(df.columns.tolist())

print("\nFinal data types:")
print(df.dtypes)

print("\nMissing values remaining:")
print(df.isna().sum())

print("\nDuplicated rows remaining:")
print(df.duplicated().sum())

print("\nIncorrect values remaining:")
print("Area:", (df["area_km2"] <= 0).sum())
print("Population:", (df["pop"] <= 0).sum())

print(
    "Life expectancy:",
    (
        (df["lifeExp"] <= 0)
        | (df["lifeExp"] > 100)
    ).sum()
)

print(
    "GDP per capita:",
    (df["gdpPercap"] <= 0).sum()
)


# 19. export the cleaned data
df.to_csv(
    output_path,
    index=False
)

print("\nCleaned data saved to:")
print(output_path)