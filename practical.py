import streamlit as st
import pandas as pd 

# Set page layout to wide
st.set_page_config(layout="wide")

# Headline
st.title("Worldwide Analysis of Quality of Life and Economic Factors")

# Subtitle
st.subheader(
    "This app enables you to explore the relationships between poverty, "
    "life expectancy, and GDP across various countries and years. "
    "Use the panels to select options and interact with the data."
)

# Create tabs
tab1, tab2, tab3 = st.tabs(["Global Overview", "Country Deep Dive", "Data Explorer"])

with tab1:
    st.write("### Global Overview")
    st.write("Content for the global overview will go here.")

with tab2:
    st.write("### Country Deep Dive")
    st.write("Content for the country deep dive will go here.")

with tab3:
    st.write("### Data Explorer")
    st.write("Content for exploring the raw data will go here.")

# Load datasetimport pandas as pd


url ="https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv"

df = pd.read_csv(url)


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
        (df["year"] >= years[0]) &
        (df["year"] <= years[1])
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