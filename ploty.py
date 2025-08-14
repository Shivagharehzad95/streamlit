import plotly.express as px
import streamlit as st

# Example: Coordinates for some countries (expand for all your data)
country_coords = {
    "United States": {"lat": 38.8977, "lon": -77.0365},
    "Germany": {"lat": 52.5200, "lon": 13.4050},
    "France": {"lat": 48.8566, "lon": 2.3522},
    "China": {"lat": 39.9042, "lon": 116.4074},
    "India": {"lat": 28.6139, "lon": 77.2090},
    "Brazil": {"lat": -15.7939, "lon": -47.8828},
    "Australia": {"lat": -35.2809, "lon": 149.1300},
    "Canada": {"lat": 45.4215, "lon": -75.6972},
    "United Kingdom": {"lat": 51.5074, "lon": -0.1278},
    "Japan": {"lat": 35.6895, "lon": 139.6917},
}

def plot_world_map(df, year_selected):
    """
    Plots a world map with GDP per capita (size) and Life Expectancy (color)
    using country capital coordinates.
    """
    df_map = df[['country', 'Life Expectancy (IHME)', 'GDP per capita', 
                 'headcount_ratio_upper_mid_income_povline']].dropna()

    # Keep only countries with coordinates
    df_map = df_map[df_map['country'].isin(country_coords.keys())].copy()

    if df_map.empty:
        st.info("No data available for the selected year to plot the map.")
        return

    # Add latitude and longitude
    df_map['lat'] = df_map['country'].apply(lambda x: country_coords[x]['lat'])
    df_map['lon'] = df_map['country'].apply(lambda x: country_coords[x]['lon'])

    fig = px.scatter_geo(
        df_map,
        lat='lat',
        lon='lon',
        hover_name='country',
        hover_data={
            "Life Expectancy (IHME)": ':.2f',
            "GDP per capita": ':.0f',
            "headcount_ratio_upper_mid_income_povline": ':.2f'
        },
        size="GDP per capita",
        color="Life Expectancy (IHME)",
        projection="natural earth",
        title=f"Global Life Expectancy & GDP ({year_selected})",
        color_continuous_scale="Turbo",
        size_max=40
    )

    fig.update_traces(
        marker=dict(
            line=dict(width=1, color="white"),
            opacity=0.8,
            sizemode="area",
            sizeref=max(df_map["GDP per capita"]) / 2000
        )
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_colorbar=dict(title="Life Exp."),
        geo=dict(
            showland=True,
            landcolor="#f2f2f2",
            showocean=True,
            oceancolor="#cce5ff",
            showcoastlines=True,
            coastlinecolor="gray",
        )
    )

    st.plotly_chart(fig, use_container_width=True)
