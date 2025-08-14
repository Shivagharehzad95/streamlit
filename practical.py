import streamlit as st
import pandas as pd

# --- Load dataset ---
url = "https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv"
df = pd.read_csv(url)

# --- Page layout ---
st.set_page_config(layout="wide")

# Headline
st.title("Worldwide Analysis of Quality of Life and Economic Factors")

# Subtitle
st.subheader(
    "This app enables you to explore the relationships between poverty, "
    "life expectancy, and GDP across various countries and years. "
    "Use the panels to select options and interact with the data."
)

# --- Create tabs ---
tab1, tab2, tab3 = st.tabs(["Global Overview", "Country Deep Dive", "Data Explorer"])

# =====================
# Tab 1: Global Overview
# =====================
with tab1:
    st.write("### Global Overview")

    # Year slider
    year_selected = st.slider(
        "Select Year",
        min_value=int(df["year"].min()),
        max_value=int(df["year"].max()),
        value=int(df["year"].min())
    )

    # Filter dataset for the selected year
    df_year = df[df["year"] == year_selected]

    # 4 Key Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        mean_life_exp = df_year["Life expectancy at birth (years)"].mean()
        st.metric("Mean Life Expectancy", f"{mean_life_exp:.2f}", "Average years people live")

    with col2:
        median_gdp = df_year["GDP per capita"].median()
        st.metric("Median GDP per Capita", f"${median_gdp:,.0f}", "Middle value of GDP per person")

    with col3:
        mean_poverty = df_year["Headcount ratio: Upper-middle-income poverty line"].mean()
        st.metric("Mean Poverty Rate", f"{mean_poverty:.2f}%", "Average % living under poverty line")

    with col4:
        num_countries = df_year["country"].nunique()
        st.metric("Number of Countries", num_countries, "Countries reporting data")

    st.write("---")
    st.write("Content for the global overview will go here.")

# =====================
# Tab 2: Country Deep Dive
# =====================
with tab2:
    st.write("### Country Deep Dive")
    st.write("Content for the country deep dive will go here.")

# =====================
# Tab 3: Data Explorer
# =====================
with tab3:
    st.write("### Data Explorer")

    # Multiselect for countries
    countries = st.multiselect(
        "Select Countries",
        options=df["country"].unique(),
        default=[]
    )

    # Year range slider
    min_year = int(df["year"].min())
    max_year = int(df["year"].max())
    years = st.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    # Filter dataset
    filtered_df = df[
        (df["year"] >= years[0]) & (df["year"] <= years[1])
    ]
    if countries:
        filtered_df = filtered_df[filtered_df["country"].isin(countries)]

    # Show filtered dataframe
    st.dataframe(filtered_df)

    # Download button
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="filtered_global_development_data.csv",
        mime="text/csv"
    )
