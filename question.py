from pathlib import Path

import pandas as pd

# 1. read the cleaned world data
base_dir = Path(__file__).resolve().parent
data_path = base_dir / "worldData_cleaned.csv"

df = pd.read_csv(data_path)

# 2. find the continent with the most countries
# find the number of unique countries in each continent
continent_country_counts = (
    df.groupby("continent")["name_long"]
    .nunique()
    .sort_values(ascending=False)
)

print("\nNumber of countries by continent:")
print(continent_country_counts)

# get the continent with most countries
continent_with_most_countries = (
    continent_country_counts.idxmax()
)
# get the number of countries in that continent
highest_country_count = (
    continent_country_counts.max()
)

print("\n1. Continent with the most countries:")
print(continent_with_most_countries)

print("Number of countries:")
print(highest_country_count)


#3. find the region with the biggest area
# grounp by region
grouped_by_region = df.groupby("region_un")

print("\nRegions:")
print(list(grouped_by_region.groups.keys()))

# get the total area for each region
region_area = grouped_by_region["area_km2"].sum()

print("\nTotal area for each region:")
print(region_area)

#find the region with the biggest area
region_with_biggest_area = region_area.idxmax()
biggest_area = region_area.max()

print("\n2. Region with the biggest area:")
print(region_with_biggest_area)
print("Total area (km^2):")
print(biggest_area)

# 4. find the country with the highest life expectancy
# rank the counries by life expectancy
life_exp_ranking = df.sort_values(
    by="lifeExp",
    ascending=False
)

print("\nCountries ordered by life expectancy:")
print(
    life_exp_ranking[
        ["name_long", "lifeExp"]
    ].head(10)
)

# find the counntry with the highest life expectancy
country_with_highest_life_exp = life_exp_ranking.iloc[0]["name_long"]
highest_life_exp = life_exp_ranking.iloc[0]["lifeExp"]

print("\n3. Country with the highest life expectancy:")
print(country_with_highest_life_exp)
print("Life expectancy:")
print(highest_life_exp)


# 5. find the higest/lowest Gdp per capita with subregion
# group by subregion
grouped_by_subregion = df.groupby("subregion")

# get the average GDP per capita for each subregion
subregion_gdp = grouped_by_subregion["gdpPercap"].mean()

# rank the subregions by average GDP per capita
subregion_gdp_ranking = subregion_gdp.sort_values(
    ascending=False
)

# find the subregion with the highest average GDP per capita
subregion_with_highest_gdp = subregion_gdp_ranking.idxmax()
highest_avg_gdp = subregion_gdp_ranking.max()

print("\n4. Subregion with the highest average GDP per capita:")
print(subregion_with_highest_gdp)
print("Average GDP per capita:")
print(highest_avg_gdp)

# find the subregion with the lowest average GDP per capita
subregion_with_lowest_gdp = subregion_gdp_ranking.idxmin()
lowest_avg_gdp = subregion_gdp_ranking.min()

print("\n5. Subregion with the lowest average GDP per capita:")
print(subregion_with_lowest_gdp)
print("Average GDP per capita:")
print(lowest_avg_gdp)


