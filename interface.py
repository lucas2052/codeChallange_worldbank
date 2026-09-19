from pathlib import Path

import pandas as pd
import streamlit as st


# 1. load the cleaned data
def load_cleaned_data(file_path):
    df = pd.read_csv(
        file_path
    )

    return df


# 2. get the available filter options
def get_filter_options(df, column):
    options = sorted(
        df[column].dropna().unique()
    )

    return options


# 3. check whether at least one filter is selected
def has_selected_filters(
    continents=None,
    regions=None,
    subregions=None,
    country_types=None
):
    return any([
        continents,
        regions,
        subregions,
        country_types
    ])


# 4. apply the selected filters
def filter_data(
    df,
    continents=None,
    regions=None,
    subregions=None,
    country_types=None
):
    filtered_df = df.copy()

    if continents:
        filtered_df = filtered_df[
            filtered_df["continent"].isin(
                continents
            )
        ]

    if regions:
        filtered_df = filtered_df[
            filtered_df["region_un"].isin(
                regions
            )
        ]

    if subregions:
        filtered_df = filtered_df[
            filtered_df["subregion"].isin(
                subregions
            )
        ]

    if country_types:
        filtered_df = filtered_df[
            filtered_df["type"].isin(
                country_types
            )
        ]

    return filtered_df


# 5. calculate summary statistics for one column
def get_summary(df, column):
    if df.empty:
        raise ValueError(
            "Cannot calculate a summary for empty data."
        )

    average_value = df[column].mean()

    max_index = df[column].idxmax()
    max_value = df.loc[
        max_index,
        column
    ]
    max_country = df.loc[
        max_index,
        "name_long"
    ]

    min_index = df[column].idxmin()
    min_value = df.loc[
        min_index,
        column
    ]
    min_country = df.loc[
        min_index,
        "name_long"
    ]

    below_average = (
        df[column] < average_value
    ).sum()

    return {
        "average": average_value,
        "max_value": max_value,
        "max_country": max_country,
        "min_value": min_value,
        "min_country": min_country,
        "below_average": below_average
    }


# 6. display the filters
def display_filters(df):
    continent_options = get_filter_options(
        df,
        "continent"
    )

    region_options = get_filter_options(
        df,
        "region_un"
    )

    subregion_options = get_filter_options(
        df,
        "subregion"
    )

    type_options = get_filter_options(
        df,
        "type"
    )

    st.subheader("Filter the data")

    filter_columns = st.columns(4)

    with filter_columns[0]:
        selected_continents = st.multiselect(
            "Continent",
            continent_options
        )

    with filter_columns[1]:
        selected_regions = st.multiselect(
            "Region",
            region_options
        )

    with filter_columns[2]:
        selected_subregions = st.multiselect(
            "Subregion",
            subregion_options
        )

    with filter_columns[3]:
        selected_types = st.multiselect(
            "Type",
            type_options
        )

    return (
        selected_continents,
        selected_regions,
        selected_subregions,
        selected_types
    )


# 7. display one summary card
def display_summary_card(
    title,
    summary,
    value_format
):
    with st.container(
        border=True,
        height=300
    ):
        st.metric(
            title,
            value_format.format(
                summary["average"]
            )
        )

        st.write(
            f'**Highest:** {summary["max_country"]}'
        )

        st.caption(
            value_format.format(
                summary["max_value"]
            )
        )

        st.write(
            f'**Lowest:** {summary["min_country"]}'
        )

        st.caption(
            value_format.format(
                summary["min_value"]
            )
        )

        st.write(
            "Below average:",
            int(summary["below_average"])
        )


# 8. display all summary cards
def display_summary_statistics(df):
    st.subheader("Summary Statistics")

    number_of_results = df["iso_a2"].nunique()

    st.write(
        f"Found {number_of_results} matching results."
    )

    area_summary = get_summary(
        df,
        "area_km2"
    )

    population_summary = get_summary(
        df,
        "pop"
    )

    life_exp_summary = get_summary(
        df,
        "lifeExp"
    )

    gdp_summary = get_summary(
        df,
        "gdpPercap"
    )

    summary_columns = st.columns(4)

    with summary_columns[0]:
        display_summary_card(
            "Average Area",
            area_summary,
            "{:,.0f} km²"
        )

    with summary_columns[1]:
        display_summary_card(
            "Average Population",
            population_summary,
            "{:,.0f}"
        )

    with summary_columns[2]:
        display_summary_card(
            "Average Life Expectancy",
            life_exp_summary,
            "{:.1f} years"
        )

    with summary_columns[3]:
        display_summary_card(
            "Average GDP per Capita",
            gdp_summary,
            "${:,.0f}"
        )


# 9. display the filtered data
def display_filtered_data(df):
    st.subheader("Filtered Data")

    st.write(
        "Number of results:",
        len(df)
    )

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True
    )


# run the Streamlit page
def main():
    # set the page
    st.set_page_config(
        page_title="World Bank Data",
        layout="wide"
    )

    # set the file path
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "worldData_cleaned.csv"

    # load the cleaned data
    df = load_cleaned_data(
        data_path
    )

    # display the page title
    st.title("World Bank Data")

    st.write(
        "Explore the cleaned World Bank data. "
        "Filter the results by continent, region, "
        "subregion, or country type."
    )

    # display the filters
    (
        selected_continents,
        selected_regions,
        selected_subregions,
        selected_types
    ) = display_filters(df)

    # require at least one filter
    if not has_selected_filters(
        continents=selected_continents,
        regions=selected_regions,
        subregions=selected_subregions,
        country_types=selected_types
    ):
        st.info(
            "Select at least one filter to explore the data."
        )
        st.stop()

    # apply the selected filters
    filtered_df = filter_data(
        df,
        continents=selected_continents,
        regions=selected_regions,
        subregions=selected_subregions,
        country_types=selected_types
    )

    # stop when no records match
    if filtered_df.empty:
        st.warning(
            "No data matches the selected filters. "
            "Please change or clear some filters."
        )
        st.stop()

    # display the summary statistics
    display_summary_statistics(
        filtered_df
    )

    # display the filtered data
    display_filtered_data(
        filtered_df
    )


# only run main() when this file is started directly
if __name__ == "__main__":
    main()




