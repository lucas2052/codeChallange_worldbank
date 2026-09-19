from pathlib import Path

import pandas as pd


# 1. load the cleaned world data
def load_cleaned_data(file_path):
    df = pd.read_csv(
        file_path
    )

    return df


# 2. check that each ISO code appears only once
def check_unique_iso_codes(df):
    if df["iso_a2"].duplicated().any():
        raise ValueError(
            "Duplicate ISO codes were found."
        )


# 3. count the countries in each continent
def count_countries_by_continent(df):
    country_counts = (
        df.groupby("continent")["iso_a2"]
        .nunique()
    )

    return country_counts


# 4. rank continents by the number of countries
def rank_continents_by_country_count(
    country_counts
):
    continent_ranking = (
        country_counts.sort_values(
            ascending=False
        )
    )

    return continent_ranking


# 5. get the continent with the most countries
def get_top_continent(continent_ranking):
    continent = continent_ranking.index[0]
    country_count = continent_ranking.iloc[0]

    return continent, country_count


# 6. calculate the total area for each region
def calculate_area_by_region(df):
    region_area = (
        df.groupby("region_un")["area_km2"]
        .sum()
    )

    return region_area


# 7. rank regions by total area
def rank_regions_by_area(region_area):
    region_ranking = (
        region_area.sort_values(
            ascending=False
        )
    )

    return region_ranking


# 8. get the region with the largest total area
def get_largest_region(region_ranking):
    region = region_ranking.index[0]
    total_area = region_ranking.iloc[0]

    return region, total_area


# 9. rank countries by life expectancy
def rank_countries_by_life_expectancy(df):
    life_expectancy_ranking = (
        df[
            [
                "name_long",
                "lifeExp"
            ]
        ]
        .sort_values(
            by="lifeExp",
            ascending=False
        )
        .reset_index(drop=True)
    )

    return life_expectancy_ranking


# 10. get the country with the highest life expectancy
def get_highest_life_expectancy(
    life_expectancy_ranking
):
    country = (
        life_expectancy_ranking
        .iloc[0]["name_long"]
    )

    life_expectancy = (
        life_expectancy_ranking
        .iloc[0]["lifeExp"]
    )

    return country, life_expectancy


# 11. calculate the average GDP for each subregion
def calculate_average_gdp_by_subregion(df):
    average_gdp = (
        df.groupby("subregion")["gdpPercap"]
        .mean()
    )

    return average_gdp


# 12. rank subregions by average GDP per capita
def rank_subregions_by_average_gdp(
    average_gdp
):
    gdp_ranking = (
        average_gdp.sort_values(
            ascending=False
        )
    )

    return gdp_ranking


# 13. get the subregion with the highest average GDP
def get_highest_average_gdp(gdp_ranking):
    subregion = gdp_ranking.index[0]
    average_gdp = gdp_ranking.iloc[0]

    return subregion, average_gdp


# 14. get the subregion with the lowest average GDP
def get_lowest_average_gdp(gdp_ranking):
    subregion = gdp_ranking.index[-1]
    average_gdp = gdp_ranking.iloc[-1]

    return subregion, average_gdp


# run the analysis
def main():
    # set the file path
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "worldData_cleaned.csv"

    # load the cleaned data
    df = load_cleaned_data(
        data_path
    )

    # check that each country has one record
    check_unique_iso_codes(df)

    # count and rank countries by continent
    continent_counts = (
        count_countries_by_continent(
            df
        )
    )

    continent_ranking = (
        rank_continents_by_country_count(
            continent_counts
        )
    )

    continent, country_count = (
        get_top_continent(
            continent_ranking
        )
    )

    print("\n1. Continent with the most countries:")
    print(continent)

    print("Number of countries:")
    print(country_count)

    print("\nNumber of countries by continent:")
    print(continent_ranking)

    # calculate and rank total area by region
    region_area = calculate_area_by_region(
        df
    )

    region_ranking = rank_regions_by_area(
        region_area
    )

    region, total_area = get_largest_region(
        region_ranking
    )

    print("\n2. Region with the largest total area:")
    print(region)

    print("Total area (km^2):")
    print(total_area)

    print("\nTotal area for each region:")
    print(region_ranking)

    # rank countries by life expectancy
    life_expectancy_ranking = (
        rank_countries_by_life_expectancy(
            df
        )
    )

    country, life_expectancy = (
        get_highest_life_expectancy(
            life_expectancy_ranking
        )
    )

    print(
        "\n3. Country with the highest "
        "life expectancy:"
    )
    print(country)

    print("Life expectancy:")
    print(life_expectancy)

    print("\nCountries ordered by life expectancy:")
    print(
            life_expectancy_ranking.head(3)
        )

    # calculate and rank average GDP by subregion
    average_gdp = (
        calculate_average_gdp_by_subregion(
            df
        )
    )

    gdp_ranking = (
        rank_subregions_by_average_gdp(
            average_gdp
        )
    )

    highest_subregion, highest_gdp = (
        get_highest_average_gdp(
            gdp_ranking
        )
    )

    lowest_subregion, lowest_gdp = (
        get_lowest_average_gdp(
            gdp_ranking
        )
    )

    print(
        "\n4.1 Subregion with the highest "
        "average GDP per capita:"
    )
    print(highest_subregion)

    print("Average GDP per capita:")
    print(highest_gdp)

    print(
        "\n4.2 Subregion with the lowest "
        "average GDP per capita:"
    )
    print(lowest_subregion)

    print("Average GDP per capita:")
    print(lowest_gdp)

    print(
            "\nAverage GDP per capita "
            "by subregion:"
        )
    print(gdp_ranking)


# only run main() when this file is started directly
if __name__ == "__main__":
    main()


