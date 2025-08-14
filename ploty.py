import plotly.express as px
import streamlit as st

def mapplot(df):
    """
    Create a scatter geo map with GDP (dot size) and Life Expectancy (color)
    df must contain columns: 'country', 'GDP', 'Life Expectancy (IHME)'
    """
    st.write("### Global Map: GDP and Life Expectancy by Country")

    # Drop rows with missing data
    df_map = df[['country', 'GDP', 'Life Expectancy (IHME)']].dropna()

    if df_map.empty:
        st.info("No data available to plot.")
        return

    fig = px.scatter_geo(
        df_map,
        locations="country",
        locationmode="country names",  # relies on correct country names
        size="GDP",
        color="Life Expectancy (IHME)",
        hover_name="country",
        title="GDP and Life Expectancy by Country",
        projection="equirectangular",
        color_continuous_scale="Turbo",
        size_max=40,
    )

    fig.update_traces(
        marker=dict(line=dict(width=1, color="white"), opacity=0.8)
    )

    fig.update_geos(
        showland=True,
        landcolor="#664423",
        showocean=True,
        oceancolor="#2b6e8e",
        showlakes=True,
        lakecolor="#467e9b",
        showcoastlines=True,
        coastlinecolor="gray",
    )

    fig.update_layout(
        title_font=dict(size=22, family="Arial", color="#333"),
        geo_bgcolor="#f9f9f9",
        margin=dict(l=0, r=0, t=60, b=0),
        coloraxis_colorbar=dict(
            title="Life Expectancy", thickness=15, len=0.5, bgcolor="#f9f9f9"
        ),
    )

    st.plotly_chart(fig, use_container_width=True)
