from pathlib import Path

import pandas as pd
import streamlit as st


# 1. set the file path
base_dir = Path(__file__).resolve().parent
data_path = base_dir / "worldData_cleaned.csv"


# 2. read the cleaned data
df = pd.read_csv(data_path)


# 3. set the page
st.set_page_config(
    page_title="World Bank Data",
    layout="wide"
)

# 4. add the page title
st.title("World Bank Data")

# 5. add a description
st.write(
    "This is a simple Streamlit app that displays the cleaned World Bank data.You can filter the data by country, year, and indicator. You can also download the filtered data as a CSV file."
)

# 6. get the unique filter options from the cleaned data
continent_options = sorted(
    df["continent"].unique()
)

region_options = sorted( 
    df["region_un"].unique()
)

subregion_options = sorted(
    df["subregion"].unique()
)

type_options = sorted(
    df["type"].unique()
)

# 7. set the filter bar 
st.subheader("Filter the data")

filter_col1, filter_col2, filter_col3, filter_col4 = (
    st.columns(4)
)

# 8. add the filters to the page
with filter_col1:
    selected_continents = st.multiselect(
        "Continent",
        continent_options
    )

with filter_col2:
    selected_regions = st.multiselect(
        "Region",
        region_options
    )

with filter_col3:
    selected_subregions = st.multiselect(
        "Subregion",
        subregion_options
    )

with filter_col4:
    selected_types = st.multiselect(
        "Type",
        type_options
    )

# 9. check if at least one filter is selected
if not (
    selected_continents
    or selected_regions
    or selected_subregions
    or selected_types
):
    st.info("Select filter to explore data.")
    st.stop()

# 10. apply the selected filters to the data
filtered_df = df.copy()

if selected_continents:
    filtered_df = filtered_df[
        filtered_df["continent"].isin(selected_continents)
    ]

if selected_regions:
    filtered_df = filtered_df[
        filtered_df["region_un"].isin(selected_regions)
    ]

if selected_subregions:
    filtered_df = filtered_df[
        filtered_df["subregion"].isin(selected_subregions)
    ]

if selected_types:
    filtered_df = filtered_df[
        filtered_df["type"].isin(selected_types)
    ]
# ensure display warning if no matches
if filtered_df.empty:
    st.warning(
        "No data matches the selected filters. "
        "Please change or clear some filters."
    )
    st.stop()

# 11. get the summary statistics

def get_summary(column):
    average_value = filtered_df[column].mean()

    max_index = filtered_df[column].idxmax()
    max_value = filtered_df.loc[max_index, column]
    max_country = filtered_df.loc[max_index, "name_long"]

    min_index = filtered_df[column].idxmin()
    min_value = filtered_df.loc[min_index, column]
    min_country = filtered_df.loc[min_index, "name_long"]

    below_average = (
        filtered_df[column] < average_value
    ).sum()

    return {
        "average": average_value,
        "max_value": max_value,
        "max_country": max_country,
        "min_value": min_value,
        "min_country": min_country,
        "below_average": below_average
    }

area_summary = get_summary("area_km2")
population_summary = get_summary("pop")
life_exp_summary = get_summary("lifeExp")
gdp_summary = get_summary("gdpPercap")

# 12. display the summary cards

st.subheader("Summary Statistics")

number_of_results = filtered_df["name_long"].nunique()

st.write(
    f"Found {number_of_results} matching results."
)

area_col, pop_col, life_col, gdp_col = st.columns(4)

# draw the area summary card
with area_col:
    with st.container(border=True,height = 300):
        st.metric(
            "Average Area",
            f'{area_summary["average"]:,.0f} km²'
        )

        st.write(
            f'**Highest:** {area_summary["max_country"]}'
        )
        st.caption(
            f'{area_summary["max_value"]:,.0f} km²'
        )

        st.write(
            f'**Lowest:** {area_summary["min_country"]}'
        )
        st.caption(
            f'{area_summary["min_value"]:,.0f} km²'
        )

        st.write(
            "Below average:",
            area_summary["below_average"]
        )
# draw the population summary card
with pop_col:
    with st.container(border=True,height = 300):
        st.metric(
            "Average Population",
            f'{population_summary["average"]:,.0f}'
        )

        st.write(
            f'**Highest:** {population_summary["max_country"]}'
        )
        st.caption(
            f'{population_summary["max_value"]:,.0f}'
        )

        st.write(
            f'**Lowest:** {population_summary["min_country"]}'
        )
        st.caption(
            f'{population_summary["min_value"]:,.0f}'
        )

        st.write(
            "Below average:",
            population_summary["below_average"]
        )
#draw the life expectancy summary card
with life_col:
    with st.container(border=True,height = 300):
        st.metric(
            "Average Life Expectancy",
            f'{life_exp_summary["average"]:.1f} years'
        )

        st.write(
            f'**Highest:** {life_exp_summary["max_country"]}'
        )
        st.caption(
            f'{life_exp_summary["max_value"]:.1f} years'
        )

        st.write(
            f'**Lowest:** {life_exp_summary["min_country"]}'
        )
        st.caption(
            f'{life_exp_summary["min_value"]:.1f} years'
        )

        st.write(
            "Below average:",
            life_exp_summary["below_average"]
        )

# draw the GDP summary card
with gdp_col:
    with st.container(border=True,height = 300):
        st.metric(
            "Average GDP per Capita",
            f'${gdp_summary["average"]:,.0f}'
        )

        st.write(
            f'**Highest:** {gdp_summary["max_country"]}'
        )
        st.caption(
            f'${gdp_summary["max_value"]:,.0f}'
        )

        st.write(
            f'**Lowest:** {gdp_summary["min_country"]}'
        )
        st.caption(
            f'${gdp_summary["min_value"]:,.0f}'
        )

        st.write(
            "Below average:",
            gdp_summary["below_average"]
        )


# 13. display the filtered data
st.subheader("Filtered Data")
st.write("Number of results:", len(filtered_df))
st.dataframe(filtered_df, use_container_width=True)




