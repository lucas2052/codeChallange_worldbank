import pandas as pd
import pytest

# import the functions to be tested
from cleandata import (
    clean_text_columns,
    convert_numeric_columns,
    find_duplicate_columns,
    find_duplicate_iso_rows,
    find_duplicate_rows,
    find_invalid_rows,
    find_missing_rows,
    get_invalid_row_mask,
    load_data,
    mark_missing_values,
    remove_duplicate_columns,
    remove_duplicate_rows,
    remove_invalid_rows,
    remove_missing_rows,
    remove_old_index_column,
    save_cleaned_data,
    validate_cleaned_data
)


# set up a valid cleaned data for testing
@pytest.fixture
def valid_cleaned_data():
    df = pd.DataFrame({
        "iso_a2": [
            "CN",
            "JP"
        ],
        "name_long": [
            "China",
            "Japan"
        ],
        "continent": [
            "Asia",
            "Asia"
        ],
        "region_un": [
            "Asia",
            "Asia"
        ],
        "subregion": [
            "Eastern Asia",
            "Eastern Asia"
        ],
        "type": [
            "Sovereign country",
            "Sovereign country"
        ],
        "area_km2": [
            100,
            200
        ],
        "pop": [
            1000,
            2000
        ],
        "lifeExp": [
            76,
            84
        ],
        "gdpPercap": [
            10000,
            30000
        ]
    })

    # set the correct data types
    text_columns = [
        "iso_a2",
        "name_long",
        "continent",
        "region_un",
        "subregion",
        "type"
    ]

    for column in text_columns:
        df[column] = df[column].astype(
            "string"
        )

    # set the correct data types for numeric columns
    integer_columns = [
        "area_km2",
        "pop",
        "lifeExp",
        "gdpPercap"
    ]

    for column in integer_columns:
        df[column] = df[column].astype(
            "int64"
        )

    return df


# 1. check that raw NA values are kept as text
def test_load_data_keeps_raw_na_values(tmp_path):
    test_file = tmp_path / "test_data.csv"

    test_file.write_text(
        "iso_a2,name_long\n"
        "NA,Namibia\n"
        "#N/A,Northern Cyprus\n",
        encoding="utf-8"
    )

    result = load_data(test_file)

    assert result.loc[0, "iso_a2"] == "NA"
    assert result.loc[1, "iso_a2"] == "#N/A"


# 2. check that the text cleaning function removes leading and trailing spaces
def test_clean_text_columns_removes_spaces():
    test_data = pd.DataFrame({
        "iso_a2": [
            " CN ",
            "JP"
        ],
        "name_long": [
            " China ",
            " Japan"
        ]
    })

    result = clean_text_columns(test_data)

    assert result["iso_a2"].tolist() == [
        "CN",
        "JP"
    ]

    assert result["name_long"].tolist() == [
        "China",
        "Japan"
    ]


# 3. check that missing values are marked correctly
def test_mark_missing_values():
    test_data = pd.DataFrame({
        "iso_a2": [
            "NA",
            "#N/A",
            ""
        ]
    })

    result = mark_missing_values(
        test_data
    )

    assert result.loc[0, "iso_a2"] == "NA"
    assert pd.isna(result.loc[1, "iso_a2"])
    assert pd.isna(result.loc[2, "iso_a2"])


# 4. check that missing rows can be found and removed
def test_find_and_remove_missing_rows():
    test_data = pd.DataFrame({
        "name_long": [
            "China",
            "Missing Country"
        ],
        "pop": [
            1000,
            None
        ]
    })

    missing_rows = find_missing_rows(
        test_data
    )

    result = remove_missing_rows(
        test_data
    )

    assert len(missing_rows) == 1

    assert missing_rows.iloc[0]["name_long"] == (
        "Missing Country"
    )

    assert result["name_long"].tolist() == [
        "China"
    ]


# 5. check that duplicate rows can be found and removed
def test_find_and_remove_duplicate_rows():
    test_data = pd.DataFrame({
        "name_long": [
            "China",
            "China",
            "China"
        ],
        "lifeExp": [
            76,
            76,
            77
        ]
    })

    duplicate_rows = find_duplicate_rows(
        test_data
    )

    result = remove_duplicate_rows(
        test_data
    )

    # The first two rows are identical
    # The third row has a different life expectancy
    assert len(duplicate_rows) == 2

    # Keep one duplicated row and the different row
    assert result["lifeExp"].tolist() == [
        76,
        77
    ]


# 6. check that rows with the same ISO code are found
def test_find_duplicate_iso_rows():
    test_data = pd.DataFrame({
        "iso_a2": [
            "CN",
            "CN",
            "JP"
        ],
        "name_long": [
            "China",
            "Different China Record",
            "Japan"
        ]
    })

    result = find_duplicate_iso_rows(
        test_data
    )

    assert result["iso_a2"].tolist() == [
        "CN",
        "CN"
    ]


# 7. check that duplicate columns are found and removed
def test_find_and_remove_duplicate_columns():
    test_data = pd.DataFrame({
        "first": [
            "A",
            "B"
        ],
        "second": [
            "A",
            "B"
        ],
        "different": [
            "C",
            "D"
        ]
    })

    duplicate_columns = find_duplicate_columns(
        test_data
    )

    result = remove_duplicate_columns(
        test_data,
        duplicate_columns
    )

    assert duplicate_columns == [
        ("first", "second")
    ]

    # Keep the first repeated column and the different column
    assert result.columns.tolist() == [
        "first",
        "different"
    ]


# 8. check that the old index column is removed
def test_remove_old_index_column():
    test_data = pd.DataFrame({
        "Unnamed: 0": [
            1,
            2
        ],
        "name_long": [
            "China",
            "Japan"
        ]
    })

    result = remove_old_index_column(
        test_data
    )

    assert "Unnamed: 0" not in result.columns
    assert "name_long" in result.columns


# 9. check that numeric values are converted and rounded
def test_convert_numeric_columns():
    test_data = pd.DataFrame({
        "area_km2": [
            "100.4",
            "100.6"
        ],
        "pop": [
            "1000",
            "2000"
        ],
        "lifeExp": [
            "75.4",
            "80.6"
        ],
        "gdpPercap": [
            "5000.4",
            "6000.6"
        ]
    })

    result = convert_numeric_columns(
        test_data
    )

    # check that the values are rounded correctly
    assert result["area_km2"].tolist() == [
        100,
        101
    ]

    assert result["lifeExp"].tolist() == [
        75,
        81
    ]

    # check that all columns are of integer type
    for column in result.columns:
        assert pd.api.types.is_integer_dtype(
            result[column]
        )


# 10. check that invalid numeric text raises an error
def test_invalid_numeric_text_raises_error():
    test_data = pd.DataFrame({
        "area_km2": [
            "not a number"
        ],
        "pop": [
            "1000"
        ],
        "lifeExp": [
            "75"
        ],
        "gdpPercap": [
            "5000"
        ]
    })

    with pytest.raises(ValueError):
        convert_numeric_columns(
            test_data
        )


# 11. check that invalid rows can be found and removed
def test_find_and_remove_invalid_rows():
    test_data = pd.DataFrame({
        "name_long": [
            "Valid Minimum",
            "Valid Maximum",
            "Invalid Area",
            "Invalid Population",
            "Invalid Life Low",
            "Invalid Life High",
            "Invalid GDP"
        ],
        "area_km2": [
            1,
            100,
            0,
            100,
            100,
            100,
            100
        ],
        "pop": [
            1,
            100,
            100,
            0,
            100,
            100,
            100
        ],
        "lifeExp": [
            1,
            100,
            70,
            70,
            0,
            101,
            70
        ],
        "gdpPercap": [
            1,
            100,
            100,
            100,
            100,
            100,
            0
        ]
    })

    invalid_mask = get_invalid_row_mask(
        test_data
    )

    invalid_rows = find_invalid_rows(
        test_data
    )

    result = remove_invalid_rows(
        test_data
    )

    # the first two rows are valid, the rest are invalid
    assert invalid_mask.tolist() == [
        False,
        False,
        True,
        True,
        True,
        True,
        True
    ]

    assert len(invalid_rows) == 5

    # valid rows should be kept, invalid rows should be removed
    assert result["name_long"].tolist() == [
        "Valid Minimum",
        "Valid Maximum"
    ]


# 12. check that valid data passes the final validation
def test_valid_data_passes_validation(
    valid_cleaned_data
):
    # no error raised means the test passes
    validate_cleaned_data(
        valid_cleaned_data
    )


# 13. check that validation rejects wrong column structure
def test_validation_rejects_wrong_columns(
    valid_cleaned_data
):
    invalid_data = valid_cleaned_data.drop(
        columns=["gdpPercap"]
    )

    with pytest.raises(
        ValueError,
        match="final columns"
    ):
        validate_cleaned_data(
            invalid_data
        )


# 14. check that validation rejects missing values
def test_validation_rejects_missing_values(
    valid_cleaned_data
):
    invalid_data = valid_cleaned_data.copy()

    invalid_data.loc[
        0,
        "name_long"
    ] = pd.NA

    with pytest.raises(
        ValueError,
        match="Missing values remain"
    ):
        validate_cleaned_data(
            invalid_data
        )


# 15. check that validation rejects duplicate rows
def test_validation_rejects_duplicate_rows(
    valid_cleaned_data
):
    duplicate_row = valid_cleaned_data.iloc[
        [0]
    ]

    invalid_data = pd.concat(
        [
            valid_cleaned_data,
            duplicate_row
        ],
        ignore_index=True
    )

    with pytest.raises(
        ValueError,
        match="Duplicate rows remain"
    ):
        validate_cleaned_data(
            invalid_data
        )


# 16. check that validation rejects duplicate ISO codes
def test_validation_rejects_duplicate_iso_codes(
    valid_cleaned_data
):
    invalid_data = valid_cleaned_data.copy()

    invalid_data.loc[
        1,
        "iso_a2"
    ] = "CN"

    with pytest.raises(
        ValueError,
        match="Duplicate ISO codes remain"
    ):
        validate_cleaned_data(
            invalid_data
        )


# 17. check that validation rejects extra spaces in text
def test_validation_rejects_extra_spaces(
    valid_cleaned_data
):
    invalid_data = valid_cleaned_data.copy()

    invalid_data.loc[
        0,
        "name_long"
    ] = " China "

    with pytest.raises(
        ValueError,
        match="contains extra spaces"
    ):
        validate_cleaned_data(
            invalid_data
        )


# 18. check that validation rejects empty text
def test_validation_rejects_empty_text(
    valid_cleaned_data
):
    invalid_data = valid_cleaned_data.copy()

    invalid_data.loc[
        0,
        "name_long"
    ] = ""

    with pytest.raises(
        ValueError,
        match="contains empty text"
    ):
        validate_cleaned_data(
            invalid_data
        )


# 19. check that validation rejects invalid ISO format
def test_validation_rejects_invalid_iso_format(
    valid_cleaned_data
):
    invalid_data = valid_cleaned_data.copy()

    invalid_data.loc[
        0,
        "iso_a2"
    ] = "CHN"

    with pytest.raises(
        ValueError,
        match="ISO codes"
    ):
        validate_cleaned_data(
            invalid_data
        )


# 20. check that validation rejects wrong numeric type
def test_validation_rejects_wrong_numeric_type(
    valid_cleaned_data
):
    invalid_data = valid_cleaned_data.copy()

    invalid_data["pop"] = (
        invalid_data["pop"]
        .astype("float64")
    )

    with pytest.raises(
        TypeError,
        match="pop is not an integer column"
    ):
        validate_cleaned_data(
            invalid_data
        )


# 21. check that validation rejects invalid range values
def test_validation_rejects_invalid_range(
    valid_cleaned_data
):
    invalid_data = valid_cleaned_data.copy()

    invalid_data.loc[
        0,
        "lifeExp"
    ] = 101

    with pytest.raises(
        ValueError,
        match="Invalid numeric values remain"
    ):
        validate_cleaned_data(
            invalid_data
        )


# 22. check that the cleaned data is saved without an index column
def test_save_cleaned_data_without_index(
    valid_cleaned_data,
    tmp_path
):
    output_path = tmp_path / "cleaned.csv"

    save_cleaned_data(
        valid_cleaned_data,
        output_path
    )

    saved_data = pd.read_csv(
        output_path,
        keep_default_na=False
    )

    assert "Unnamed: 0" not in saved_data.columns

    assert saved_data.columns.tolist() == (
        valid_cleaned_data.columns.tolist()
    )