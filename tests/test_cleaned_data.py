import pandas as pd
import pytest

from cleandata import (
    clean_text_columns,
    convert_numeric_columns,
    find_duplicate_columns,
    find_duplicate_rows,
    find_invalid_rows,
    find_missing_rows,
    get_invalid_row_mask,
    load_data,
    remove_duplicate_columns,
    remove_duplicate_rows,
    remove_invalid_rows,
    remove_missing_rows,
    remove_old_index_column,
    save_cleaned_data,
    validate_cleaned_data
)


# 1. set up a valid cleaned data for testing
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

    # 2. set the correct data types
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

    # 3. set the correct data types for numeric columns
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


# 4. set up a temporary csv file that aligns with the valid cleaned date
def test_load_data_handles_iso_codes(tmp_path):
    test_file = tmp_path / "test_data.csv"

    test_file.write_text(
        "iso_a2,name_long\n"
        "NA,Namibia\n"
        "#N/A,Northern Cyprus\n",
        encoding="utf-8"
    )

    result = load_data(test_file)

    # make sure the NA is read as a string and not converted to NaN
    assert result.loc[0, "iso_a2"] == "NA"

    # make sure the #N/A is read as a missing value
    assert pd.isna(result.loc[1, "iso_a2"])


# 5. check that the text cleaning function removes leading and trailing spaces
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


# 6. check that the text cleaning function marks empty text as missing
def test_clean_text_columns_marks_empty_text_as_missing():
    test_data = pd.DataFrame({
        "name_long": [
            "China",
            "   "
        ]
    })

    result = clean_text_columns(test_data)

    assert result.loc[0, "name_long"] == "China"
    assert pd.isna(result.loc[1, "name_long"])


# 7. check that the text cleaning function does not modify the original data
def test_clean_text_columns_keeps_original_data():
    test_data = pd.DataFrame({
        "name_long": [
            " China "
        ]
    })

    clean_text_columns(test_data)

    assert test_data.loc[0, "name_long"] == (
        " China "
    )


# 8. check that missing rows can be found and removed
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


# 9. check that valid data is not removed when looking for missing rows
def test_remove_missing_rows_keeps_valid_data():
    test_data = pd.DataFrame({
        "name_long": [
            "China",
            "Japan"
        ],
        "pop": [
            1000,
            2000
        ]
    })

    result = remove_missing_rows(
        test_data
    )

    pd.testing.assert_frame_equal(
        result,
        test_data
    )


# 10. check that duplicate rows can be found and removed
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

    # last two rows are duplicates, but the third row has a different lifeExp value
    assert len(duplicate_rows) == 2

    # lifeExp should be 76 for the first two rows, and 77 for the third row
    assert result["lifeExp"].tolist() == [
        76,
        77
    ]


# 11. check that duplicate columns are found and removed
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

    # the second column should be removed, leaving only the first and different columns
    assert result.columns.tolist() == [
        "first",
        "different"
    ]


# 12. check that valid data is not removed when looking for duplicate columns
def test_remove_duplicate_columns_keeps_unique_columns():
    test_data = pd.DataFrame({
        "first": [
            "A",
            "B"
        ],
        "second": [
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

    assert duplicate_columns == []

    pd.testing.assert_frame_equal(
        result,
        test_data
    )


# 13. check that old index columns can be found and removed
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


# 13. check that old index columns can be found and removed
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


# 14. check that missing old index columns are allowed
def test_missing_old_index_column_is_allowed():
    test_data = pd.DataFrame({
        "name_long": [
            "China"
        ]
    })

    result = remove_old_index_column(
        test_data
    )

    pd.testing.assert_frame_equal(
        result,
        test_data
    )


# 15. check the numeric conversion function correctly converts and rounds values
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


# check the numeric conversion function raises an error for invalid text
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


# 16. check that invalid rows can be found and removed
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


# 17. check that valid rows are not removed
def test_valid_rows_are_not_removed(
    valid_cleaned_data
):
    result = remove_missing_rows(
        valid_cleaned_data
    )

    result = remove_duplicate_rows(
        result
    )

    result = remove_invalid_rows(
        result
    )

    pd.testing.assert_frame_equal(
        result,
        valid_cleaned_data
    )


# 18. check that valid data passes the final validation
def test_valid_data_passes_validation(
    valid_cleaned_data
):
    # no error raised means the test passes
    validate_cleaned_data(
        valid_cleaned_data
    )


# 19. check that validation rejects wrong column structure
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


# 20. check that validation rejects missing values
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


# 21. check that validation rejects duplicate rows
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


# 22. check that validation rejects extra spaces in text
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


# 23. check that validation rejects empty text
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


# 24. check that validation rejects invalid ISO format
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


# 25. check that validation rejects wrong numeric type
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


# 26. check that validation rejects invalid range values
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


# 27. check that the cleaned data is saved without an index column
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