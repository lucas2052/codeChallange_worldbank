from pathlib import Path
import pandas as pd


# 1. load the data and keep NA as Namibia's ISO code
def load_data(file_path):
    df = pd.read_csv(
        file_path,
        keep_default_na=False
    )
    return df


# 2.check basic information about the original data
def show_original_data(df):
    print(
        f"Original data: "
        f"{len(df)} rows, "
        f"{len(df.columns)} columns"
    )


# 3. remove spaces before and after text values
def clean_text_columns(df):
    df = df.copy()

    # find columns stored as object or string
    text_columns = (
        df.select_dtypes(
            include=["object", "string"]
        )
        .columns
        .tolist()
    )
    # remove spaces before and after each text value
    for column in text_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    return df

# 4. mark empty text and "#N/A" as missing values
def mark_missing_values(df):
    return df.replace(
        ["#N/A", ""],
        pd.NA
    )

# 5. find rows that contain missing values
def find_missing_rows(df):
    return df[
        df.isna().any(axis=1)
    ]


# 6. remove rows that contain missing values
def remove_missing_rows(df):
    return df.dropna()


# 7. find columns that contain the same values
def find_duplicate_columns(df):
    duplicate_columns = []

    columns = df.columns.tolist()

    # compare each column with every column after it
    for first_index in range(len(columns)):
        for second_index in range(
            first_index + 1,
            len(columns)
        ):
            # get the column names for the two indices
            first_column = columns[first_index]
            second_column = columns[second_index]

            # check whether both columns contain the same values
            if df[first_column].equals(
                df[second_column]
            ):
                # save the pair of duplicate columns
                duplicate_columns.append(
                    (
                        first_column,
                        second_column
                    )
                )

    return duplicate_columns


# 8. remove duplicate columns and keep the first column
def remove_duplicate_columns(
    df,
    duplicate_column_pairs
):
    columns_to_remove = []

    # keep the first column and collect the second column from each pair
    for _, second_column in duplicate_column_pairs:
        if second_column not in columns_to_remove:
            columns_to_remove.append(
                second_column
            )
    # remove the collected duplicate columns
    return df.drop(
        columns=columns_to_remove
    )


# 9. find all rows involved in duplication
def find_duplicate_rows(df):
    return df[
        df.duplicated(keep=False)
    ]


# 10. remove completely duplicated rows
def remove_duplicate_rows(df):
    return df.drop_duplicates()


# 11. find rows with the same ISO code
def find_duplicate_iso_rows(df):
    return df[
        df["iso_a2"].duplicated(
            keep=False
        )
    ]

# 12. remove the old CSV index column if it exists
def remove_old_index_column(df):
    return df.drop(
        columns=["Unnamed: 0"],
        errors="ignore"
    )

# 13. convert the numeric columns to integers
def convert_numeric_columns(df):
    df = df.copy()

    # list the numeric columns to be converted to integers
    integer_columns = [
        "area_km2",
        "pop",
        "lifeExp",
        "gdpPercap"
    ]

    # convert each numeric column to integer
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


# 14. mark rows with invalid numeric values
def get_invalid_row_mask(df):

    # check each numeric field against its accepted range
    invalid_area = (
        (df["area_km2"] < 1)
        | (df["area_km2"] > 17_100_000)
    )
    
    invalid_population = (
        (df["pop"] < 800)
        | (df["pop"] > 1_400_000_000)
    )

    invalid_life_exp = (
        (df["lifeExp"] < 40)
        | (df["lifeExp"] > 86)
    )

    invalid_gdp = (
        (df["gdpPercap"] < 200)
        | (df["gdpPercap"] > 200_000)
    )

    # combine the invalid masks to find all rows with invalid numeric values
    return (
        invalid_area
        | invalid_population
        | invalid_life_exp
        | invalid_gdp
    )

# 15. find rows with invalid numeric values
def find_invalid_rows(df):

    # get the mask for invalid rows
    invalid_row_mask = get_invalid_row_mask(df)

    return df[
        invalid_row_mask
    ]

# 16. remove rows with invalid values
def remove_invalid_rows(df):
    invalid_row_mask = get_invalid_row_mask(df)

    # keep the valid rows 
    return df[
        ~invalid_row_mask
    ]

# 17. validate the cleaned data before saving
def validate_cleaned_data(df):
    # define the expected, text, and integer columns
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

    # check the columns
    if df.columns.tolist() != expected_columns:
        raise ValueError(
            "The final columns are incorrect."
        )

    # check missing values
    if df.isna().any().any():
        raise ValueError(
            "Missing values remain."
        )

    # check repeated rows
    if df.duplicated().any():
        raise ValueError(
            "Duplicate rows remain."
        )

    # check repeated ISO codes
    if not find_duplicate_iso_rows(df).empty:
        raise ValueError(
            "Duplicate ISO codes remain."
        )

    # check the text columns
    for column in text_columns:
        if not pd.api.types.is_string_dtype(
            df[column]
        ):
            raise TypeError(
                f"{column} is not a text column."
            )

        if df[column].eq("").any():
            raise ValueError(
                f"{column} contains empty text."
            )

        if df[column].str.strip().ne(
            df[column]
        ).any():
            raise ValueError(
                f"{column} contains extra spaces."
            )

    # check the ISO code format matches two uppercase letters
    if not df["iso_a2"].str.fullmatch(
        r"[A-Z]{2}"
    ).all():
        raise ValueError(
            "Some ISO codes are invalid."
        )

    # check the number columns are integers
    for column in integer_columns:
        if not pd.api.types.is_integer_dtype(
            df[column]
        ):
            raise TypeError(
                f"{column} is not an integer column."
            )

    # check the number ranges are valid
    if not find_invalid_rows(df).empty:
        raise ValueError(
            "Invalid numeric values remain."
        )

# 18. view the final cleaned data information
def show_final_data(df):
    print(
        f"Final data: "
        f"{len(df)} rows, "
        f"{len(df.columns)} columns"
    )

# 19. save the cleaned data without the pandas index
def save_cleaned_data(df, output_path):
    df.to_csv(
        output_path,
        index=False
    )

    print("\nCleaned data saved to:")
    print(output_path)


# run the cleaning process
def main():
    # set the input and output paths
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "worldData.csv"
    output_path = base_dir / "worldData_cleaned.csv"

    # load and inspect the original data
    df = load_data(input_path)
    show_original_data(df)

    # clean the text columns
    df = clean_text_columns(df)

    # update the DataFrame to mark missing values
    df = mark_missing_values(df)

    # find rows with missing values
    missing_count = len(
        find_missing_rows(df)
    )

    # update the DataFrame to remove rows with missing values
    df = remove_missing_rows(df)

    # find repeated columns
    duplicate_columns = find_duplicate_columns(
        df
    )

    # remove the repeated columns and keep the first column
    removed_columns = [
        second_column
        for _, second_column
        in duplicate_columns
    ]

    # update the DataFrame to remove the repeated columns
    df = remove_duplicate_columns(
        df,
        duplicate_columns
    )

    # remove the old CSV index column
    old_index_removed = (
        "Unnamed: 0" in df.columns
    )

    # update the DataFrame to remove the old index column if it exists
    df = remove_old_index_column(df)

    # find and remove completely repeated rows
    duplicate_count = (
        df.duplicated().sum()
    )
    # update the DataFrame to remove the completely repeated rows
    df = remove_duplicate_rows(df)

    # convert the numeric columns
    df = convert_numeric_columns(df)

    # find and remove invalid numeric rows
    invalid_count = len(
        find_invalid_rows(df)
    )

    # update the DataFrame to remove the invalid numeric rows
    df = remove_invalid_rows(df)

    # check repeated ISO codes
    duplicate_iso_count = len(
        find_duplicate_iso_rows(df)
    )

    # show a short cleaning summary
    print("\nCleaning summary")
    print("----------------")
    print(
        "Missing rows removed:",
        missing_count
    )
    print(
        "Repeated columns removed:",
        removed_columns
    )
    print(
        "Old CSV index removed:",
        old_index_removed
    )
    print(
        "Duplicate rows removed:",
        duplicate_count
    )
    print(
        "Invalid numeric rows removed:",
        invalid_count
    )
    print(
        "Repeated ISO codes remaining:",
        duplicate_iso_count
    )

    # validate the final data
    validate_cleaned_data(df)

    print("Validation passed.")

    # show and save the cleaned data
    show_final_data(df)

    save_cleaned_data(
        df,
        output_path
    )

# run main() only when this file is executed directly
if __name__ == "__main__":
    main()