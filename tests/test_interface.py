from pathlib import Path

import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from interface import (
    filter_data,
    get_filter_options,
    get_summary,
    has_selected_filters,
    load_cleaned_data
)


# create sample data used by the interface tests
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "iso_a2": [
            "CN",
            "JP",
            "FR",
            "GL"
        ],
        "name_long": [
            "China",
            "Japan",
            "France",
            "Greenland"
        ],
        "continent": [
            "Asia",
            "Asia",
            "Europe",
            "North America"
        ],
        "region_un": [
            "Asia",
            "Asia",
            "Europe",
            "Americas"
        ],
        "subregion": [
            "Eastern Asia",
            "Eastern Asia",
            "Western Europe",
            "Northern America"
        ],
        "type": [
            "Sovereign country",
            "Sovereign country",
            "Sovereign country",
            "Dependency"
        ],
        "area_km2": [
            9_600_000,
            378_000,
            552_000,
            2_166_000
        ],
        "pop": [
            1_364_000_000,
            127_000_000,
            66_000_000,
            56_000
        ],
        "lifeExp": [
            76,
            84,
            82,
            72
        ],
        "gdpPercap": [
            7_600,
            38_000,
            43_000,
            50_000
        ]
    })


# check that cleaned data can be loaded from a CSV file
def test_load_cleaned_data(
    sample_data,
    tmp_path
):
    file_path = (
        tmp_path
        / "test_data.csv"
    )

    sample_data.to_csv(
        file_path,
        index=False
    )

    result = load_cleaned_data(
        file_path
    )

    pd.testing.assert_frame_equal(
        result,
        sample_data
    )


# check that filter options are unique and sorted
def test_get_filter_options(sample_data):
    options = get_filter_options(
        sample_data,
        "continent"
    )

    assert options == [
        "Asia",
        "Europe",
        "North America"
    ]


# check that no filters are selected
def test_no_selected_filters():
    result = has_selected_filters()

    assert result is False


# check that one or more selected filters are found
@pytest.mark.parametrize(
    "selected_filters",
    [
        {
            "continents": ["Asia"]
        },
        {
            "regions": ["Europe"]
        },
        {
            "subregions": ["Eastern Asia"]
        },
        {
            "country_types": ["Dependency"]
        }
    ]
)
def test_selected_filters_are_found(
    selected_filters
):
    result = has_selected_filters(
        **selected_filters
    )

    assert result is True


# check filtering by one field
def test_filter_by_continent(sample_data):
    result = filter_data(
        sample_data,
        continents=["Asia"]
    )

    assert result["name_long"].tolist() == [
        "China",
        "Japan"
    ]


# check filtering by several fields
def test_filter_by_multiple_fields(
    sample_data
):
    result = filter_data(
        sample_data,
        continents=["Asia"],
        regions=["Asia"],
        subregions=["Eastern Asia"],
        country_types=[
            "Sovereign country"
        ]
    )

    assert result["name_long"].tolist() == [
        "China",
        "Japan"
    ]


# check that selected filters use AND logic
def test_filters_use_and_logic(sample_data):
    result = filter_data(
        sample_data,
        continents=["Asia"],
        regions=["Europe"]
    )

    assert result.empty


# check that an unknown option returns no results
def test_filter_with_no_matching_data(
    sample_data
):
    result = filter_data(
        sample_data,
        subregions=[
            "Unknown subregion"
        ]
    )

    assert result.empty


# check summary statistics
def test_get_summary(sample_data):
    summary = get_summary(
        sample_data,
        "lifeExp"
    )

    assert summary["average"] == 78.5
    assert summary["max_value"] == 84
    assert summary["max_country"] == "Japan"
    assert summary["min_value"] == 72
    assert summary["min_country"] == "Greenland"
    assert summary["below_average"] == 2


# check summary statistics with one record
def test_get_summary_with_one_record(
    sample_data
):
    one_record = sample_data.iloc[
        [0]
    ]

    summary = get_summary(
        one_record,
        "pop"
    )

    assert summary["average"] == 1_364_000_000
    assert summary["max_country"] == "China"
    assert summary["min_country"] == "China"
    assert summary["below_average"] == 0


# check that summary statistics reject empty data
def test_get_summary_rejects_empty_data(
    sample_data
):
    empty_data = sample_data.iloc[
        0:0
    ]

    with pytest.raises(
        ValueError,
        match="Cannot calculate a summary for empty data"
    ):
        get_summary(
            empty_data,
            "pop"
        )


# check that the Streamlit page starts successfully
def test_interface_starts():
    project_dir = (
        Path(__file__)
        .resolve()
        .parent
        .parent
    )

    interface_path = (
        project_dir
        / "interface.py"
    )

    app = AppTest.from_file(
        str(interface_path)
    ).run()

    assert len(app.exception) == 0

    assert app.title[0].value == (
        "World Bank Data"
    )

    assert app.info[0].value == (
        "Select at least one filter "
        "to explore the data."
    )