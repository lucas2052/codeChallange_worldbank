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

    # check that each country or area has one record
    if df["iso_a2"].duplicated().any():
        raise ValueError(
            "Duplicate ISO codes were found."
        )


# 3. count the countries in each continent
def count_countries_by_continent(df):
    # group records by continent and count unique ISO codes
    country_counts = (
        df.groupby("continent")["iso_a2"]
        .nunique()
    )
    
    return country_counts


# 4. rank continents by the number of countries
def rank_continents_by_country_count(
    country_counts
):
    # sort from the largest to the smallest
    continent_ranking = (
        country_counts.sort_values(
            ascending=False
        )
    )

    return continent_ranking


# 5. get the continent with the most countries
def get_top_continent(continent_ranking):

    # the first item has the highest country count
    continent = continent_ranking.index[0]
    country_count = continent_ranking.iloc[0]

    # return the continent and its country count
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
    # sort from the largest total area to the smallest
    region_ranking = (
        region_area.sort_values(
            ascending=False
        )
    )

    return region_ranking


# 8. get the region with the largest total area
def get_largest_region(region_ranking):
    # get the first item which is the region with the largest area
    region = region_ranking.index[0]
    total_area = region_ranking.iloc[0]

    return region, total_area


# 9. rank countries by life expectancy
def rank_countries_by_life_expectancy(df):

    # keep the country name and life expectancy for ranking
    life_expectancy_ranking = (
        df[
            [
                "name_long",
                "lifeExp"
            ]
        ]
        # sort life expectancy from highest to lowest
        .sort_values(
            by="lifeExp",
            ascending=False
        )
        .reset_index(drop=True)
    )

    # return the ranked records
    return life_expectancy_ranking


# 10. get the country with the highest life expectancy
def get_highest_life_expectancy(
    life_expectancy_ranking
):
    # get the first row that contains the highest life expectancy
    country = (
        life_expectancy_ranking
        .iloc[0]["name_long"]
    )

    life_expectancy = (
        life_expectancy_ranking
        .iloc[0]["lifeExp"]
    )

    return country, life_expectancy


# 11. calculate the average GDP per capita for each subregion
def calculate_average_gdp_by_subregion(df):

    # group by subregion and calculate the arithmetic mean
    average_gdp = (
        df.groupby("subregion")["gdpPercap"]
        .mean()
    )

    return average_gdp


# 12. rank subregions by average GDP per capita
def rank_subregions_by_average_gdp(
    average_gdp
): 
    # sort from the highest average to the lowest
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

    # return the subregion and its average GDP
    return subregion, average_gdp


# 14. get the subregion with the lowest average GDP per capita
def get_lowest_average_gdp(gdp_ranking):

    # the last item has the lowest average GDP
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

    # select the top continent
    continent, country_count = (
        get_top_continent(
            continent_ranking
        )
    )

    # display the first question's answer
    print("\n1. Continent with the most countries:")
    print(continent)

    print("Number of countries:")
    print(country_count)

    print("\nNumber of countries by continent:")
    print(continent_ranking)

    # calculate the total area by region
    region_area = calculate_area_by_region(
        df
    )

    # rank the total area by region
    region_ranking = rank_regions_by_area(
        region_area
    )

    # select the largest total area by region
    region, total_area = get_largest_region(
        region_ranking
    )

    # display the second question's answer
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

    # select the country with the highest life expectancy
    country, life_expectancy = (
        get_highest_life_expectancy(
            life_expectancy_ranking
        )
    )

    # display the third question's answer
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

    # select the subregion with the highest average GDP per capita
    highest_subregion, highest_gdp = (
        get_highest_average_gdp(
            gdp_ranking
        )
    )

    # select the subregion with the lowest gdp 
    lowest_subregion, lowest_gdp = (
        get_lowest_average_gdp(
            gdp_ranking
        )
    )

    # display the final question's answer 
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


# run main() only when this file is executed directly
if __name__ == "__main__":
    main()


