import pandas as pd
import pytest

from question import (
    calculate_area_by_region,
    calculate_average_gdp_by_subregion,
    check_unique_iso_codes,
    count_countries_by_continent,
    get_highest_average_gdp,
    get_highest_life_expectancy,
    get_largest_region,
    get_lowest_average_gdp,
    get_top_continent,
    load_cleaned_data,
    rank_continents_by_country_count,
    rank_countries_by_life_expectancy,
    rank_regions_by_area,
    rank_subregions_by_average_gdp
)


# Set up sample data for testing
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "iso_a2": [
            "CN",
            "JP",
            "IN",
            "FR",
            "DE",
            "BR"
        ],
        "name_long": [
            "China",
            "Japan",
            "India",
            "France",
            "Germany",
            "Brazil"
        ],
        "continent": [
            "Asia",
            "Asia",
            "Asia",
            "Europe",
            "Europe",
            "South America"
        ],
        "region_un": [
            "Asia",
            "Asia",
            "Asia",
            "Europe",
            "Europe",
            "Americas"
        ],
        "subregion": [
            "Eastern Asia",
            "Eastern Asia",
            "Southern Asia",
            "Western Europe",
            "Western Europe",
            "South America"
        ],
        "area_km2": [
            100,
            200,
            100,
            50,
            70,
            500
        ],
        "lifeExp": [
            76,
            84,
            70,
            82,
            81,
            75
        ],
        "gdpPercap": [
            10000,
            30000,
            20000,
            40000,
            50000,
            15000
        ]
    })


# Check that cleaned data can be loaded
def test_load_cleaned_data(
    sample_data,
    tmp_path
):
    test_file = tmp_path / "cleaned.csv"

    sample_data.to_csv(
        test_file,
        index=False
    )

    result = load_cleaned_data(
        test_file
    )

    pd.testing.assert_frame_equal(
        result,
        sample_data
    )


# Check unique and repeated ISO codes
def test_check_unique_iso_codes(sample_data):
    check_unique_iso_codes(
        sample_data
    )

    invalid_data = sample_data.copy()

    invalid_data.loc[
        1,
        "iso_a2"
    ] = "CN"

    with pytest.raises(
        ValueError,
        match="Duplicate ISO codes"
    ):
        check_unique_iso_codes(
            invalid_data
        )


# Check the continent with the most countries
def test_continent_country_ranking(sample_data):
    country_counts = (
        count_countries_by_continent(
            sample_data
        )
    )

    ranking = (
        rank_continents_by_country_count(
            country_counts
        )
    )

    continent, country_count = (
        get_top_continent(
            ranking
        )
    )

    assert country_counts["Asia"] == 3
    assert ranking.index[0] == "Asia"
    assert continent == "Asia"
    assert country_count == 3


# Check the region with the largest total area
def test_region_area_ranking(sample_data):
    region_area = calculate_area_by_region(
        sample_data
    )

    ranking = rank_regions_by_area(
        region_area
    )

    region, total_area = get_largest_region(
        ranking
    )

    assert region_area["Asia"] == 400
    assert ranking.index[0] == "Americas"
    assert region == "Americas"
    assert total_area == 500


# Check the country with the highest life expectancy
def test_life_expectancy_ranking(sample_data):
    ranking = (
        rank_countries_by_life_expectancy(
            sample_data
        )
    )

    country, life_expectancy = (
        get_highest_life_expectancy(
            ranking
        )
    )

    assert ranking.iloc[0]["name_long"] == "Japan"
    assert country == "Japan"
    assert life_expectancy == 84


# Check the highest and lowest average GDP by subregion
def test_subregion_gdp_ranking(sample_data):
    average_gdp = (
        calculate_average_gdp_by_subregion(
            sample_data
        )
    )

    ranking = (
        rank_subregions_by_average_gdp(
            average_gdp
        )
    )

    highest_subregion, highest_gdp = (
        get_highest_average_gdp(
            ranking
        )
    )

    lowest_subregion, lowest_gdp = (
        get_lowest_average_gdp(
            ranking
        )
    )

    assert average_gdp["Eastern Asia"] == 20000

    assert highest_subregion == "Western Europe"
    assert highest_gdp == 45000

    assert lowest_subregion == "South America"
    assert lowest_gdp == 15000


