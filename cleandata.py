from pathlib import Path
import pandas as pd


# 1.load the world data and keep "NA" as Namibia's ISO code
def load_data(file_path):
    return pd.read_csv(
        file_path,
        keep_default_na=False,
        na_values=["#N/A", ""]
    )


# 2.check basic information about the original data
def show_original_data(df):
    print("Original dataset shape:")
    print(df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData information:")
    df.info()

    print("\nSummary statistics:")
    print(df.describe())


# 3. remove spaces around text and mark empty text as missing
def clean_text_columns(df):
    df = df.copy()

    text_columns = (
        df.select_dtypes(
            include=["object", "string"]
        )
        .columns
        .tolist()
    )

    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    df[text_columns] = (
        df[text_columns]
        .replace("", pd.NA)
    )

    return df

# 4. check all rows that contain missing values
def find_missing_rows(df):
    return df[
        df.isna().any(axis=1)
    ]


# 5. remove rows that contain missing values
def remove_missing_rows(df):
    return df.dropna()


# 6. check all rows involved in duplication
def find_duplicate_rows(df):
    return df[
        df.duplicated(keep=False)
    ]


# 7. remove completely duplicated rows
def remove_duplicate_rows(df):
    return df.drop_duplicates()


# 8. find columns that contain the same values
def find_duplicate_columns(df):
    duplicate_columns = []

    columns = df.columns.tolist()

    for first_index in range(len(columns)):
        for second_index in range(
            first_index + 1,
            len(columns)
        ):
            first_column = columns[first_index]
            second_column = columns[second_index]

            if df[first_column].equals(
                df[second_column]
            ):
                duplicate_columns.append(
                    (
                        first_column,
                        second_column
                    )
                )

    return duplicate_columns

# 9. remove repeated columns and keep the first column
def remove_duplicate_columns(
    df,
    duplicate_column_pairs
):
    
    columns_to_remove = []

    for first_column, second_column in duplicate_column_pairs:
        if second_column not in columns_to_remove:
            columns_to_remove.append(
                second_column
            )

    return df.drop(
        columns=columns_to_remove
    )

# 10. remove the old CSV index column if it exists
def remove_old_index_column(df):
    return df.drop(
        columns=["Unnamed: 0"],
        errors="ignore"
    )

# 11. convert the numeric columns to integers
def convert_numeric_columns(df):
    df = df.copy()

    integer_columns = [
        "area_km2",
        "pop",
        "lifeExp",
        "gdpPercap"
    ]

    for column in integer_columns:
        df[column] = (
            pd.to_numeric(
                df[column],
                errors="raise"
            )
            .round()
            .astype("int64")
        )

    return df


# 12. mark rows with invalid numeric values
def get_invalid_row_mask(df):
    invalid_area = df["area_km2"] <= 0
    invalid_population = df["pop"] <= 0

    invalid_life_exp = (
        (df["lifeExp"] <= 0)
        | (df["lifeExp"] > 100)
    )

    invalid_gdp = df["gdpPercap"] <= 0

    return (
        invalid_area
        | invalid_population
        | invalid_life_exp
        | invalid_gdp
    )

# 13. find rows with invalid numeric values
def find_invalid_rows(df):
    invalid_row_mask = get_invalid_row_mask(df)

    return df[
        invalid_row_mask
    ]

# 14. remove rows with invalid values
def remove_invalid_rows(df):
    invalid_row_mask = get_invalid_row_mask(df)

    return df[
        ~invalid_row_mask
    ]

# 15. validate the cleaned data before saving
def validate_cleaned_data(df):
    expected_columns = [
        "iso_a2",
        "name_long",
        "continent",
        "region_un",
        "subregion",
        "type",
        "area_km2",
        "pop",
        "lifeExp",
        "gdpPercap"
    ]

    text_columns = [
        "iso_a2",
        "name_long",
        "continent",
        "region_un",
        "subregion",
        "type"
    ]

    integer_columns = [
        "area_km2",
        "pop",
        "lifeExp",
        "gdpPercap"
    ]

    # Check the final columns
    if df.columns.tolist() != expected_columns:
        raise ValueError(
            "The final columns are incorrect."
        )

    # Check missing values
    if df.isna().any().any():
        raise ValueError(
            "Missing values remain."
        )

    # Check duplicate rows
    if df.duplicated().any():
        raise ValueError(
            "Duplicate rows remain."
        )

    # Check text types and spaces
    for column in text_columns:
        if not pd.api.types.is_string_dtype(
            df[column]
        ):
            raise TypeError(
                f"{column} is not a text column."
            )

        if df[column].str.strip().ne(
            df[column]
        ).any():
            raise ValueError(
                f"{column} contains extra spaces."
            )

        if df[column].eq("").any():
            raise ValueError(
                f"{column} contains empty text."
            )

    # Check the ISO code format
    if not df["iso_a2"].str.fullmatch(
        r"[A-Z]{2}"
    ).all():
        raise ValueError(
            "Some ISO codes are invalid."
        )

    # Check integer types
    for column in integer_columns:
        if not pd.api.types.is_integer_dtype(
            df[column]
        ):
            raise TypeError(
                f"{column} is not an integer column."
            )

    # Check numeric ranges
    if not find_invalid_rows(df).empty:
        raise ValueError(
            "Invalid numeric values remain."
        )

# 16. view the final cleaned data
def show_final_data(df):
    print("\nFinal dataset shape:")
    print(df.shape)

    print("\nFinal columns:")
    print(df.columns.tolist())

    print("\nFinal data types:")
    print(df.dtypes)

# 17. save the cleaned data without the pandas index
def save_cleaned_data(df, output_path):
    df.to_csv(
        output_path,
        index=False
    )

    print("\nCleaned data saved to:")
    print(output_path)


# run the main process
def main():
    # 1. set the input and output paths
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "worldData.csv"
    output_path = base_dir / "worldData_cleaned.csv"

    # 2. load the original data
    df = load_data(input_path)

    # 3. check the original data
    show_original_data(df)

    # 4. clean the invalid special text 
    df = clean_text_columns(df)

    # 5. find missing rows and remove them
    missing_rows = find_missing_rows(df)

    print("\nRows with missing values:")
    print(missing_rows)

    print("\nNumber of rows with missing values:")
    print(len(missing_rows))

    df = remove_missing_rows(df)

    print("\nDataset shape after removing missing values:")
    print(df.shape)

    # 6. find and remove duplicate rows
    duplicate_rows = find_duplicate_rows(df)

    print("\nDuplicate rows:")
    print(duplicate_rows)

    print("\nNumber of extra duplicate rows:")
    print(df.duplicated().sum())

    df = remove_duplicate_rows(df)

    print("\nDataset shape after removing duplicate rows:")
    print(df.shape)

    # 7. find duplicated columns
    duplicate_columns = find_duplicate_columns(df)
    print("\nColumns with the same values:")
    print(duplicate_columns)

    # 8. remove duplicate columns
    df = remove_duplicate_columns(df, duplicate_columns)

    # 9. remove the old CSV index column
    df = remove_old_index_column(df)

    # 10. convert the number columns to integers
    df = convert_numeric_columns(df)

    # 11. find values that are incorrect ranges or types
    invalid_rows = find_invalid_rows(df)

    print("\nRows with incorrect values:")
    print(invalid_rows)

    print("\nNumber of rows with incorrect values:")
    print(len(invalid_rows))

    # 12. remove rows that contain incorrect values
    df = remove_invalid_rows(df)

    print("\nDataset shape after removing incorrect values:")
    print(df.shape)

    # 13. Validate the cleaned data
    validate_cleaned_data(df)
    print("\nFinal validation passed.")

    # 14. view the cleaned data
    show_final_data(df)

    # 15. Export the cleaned data
    save_cleaned_data(
        df,
        output_path
    )


#  only run main() when this file is started directly
if __name__ == "__main__":
    main()