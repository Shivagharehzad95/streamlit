import plotly.express as px
import streamlit as st

def plot_world_map(df_year):
    """
    Create a global map using Plotly scatter_geo.
    df_year must contain columns:
    'country', 'Life Expectancy (IHME)', 'GDP per capita', 'headcount_ratio_upper_mid_income_povline'
    """
    st.write("### Task 7: Global Map")

    df_map = df_year[['country', 'Life Expectancy (IHME)', 'GDP per capita', 'headcount_ratio_upper_mid_income_povline']].dropna()

    if df_map.empty:
        st.info("No data available for the selected year to plot the map.")
    else:
        fig = px.scatter_geo(
            df_map,
            locations="country",
            locationmode="country names",
            hover_name="country",
            hover_data={
                "Life Expectancy (IHME)": ':.2f',
                "GDP per capita": ':.0f',
                "headcount_ratio_upper_mid_income_povline": ':.2f'
            },
            color="Life Expectancy (IHME)",
            size="GDP per capita",
            projection="natural earth",
            title=None,
        )

        fig.update_traces(
            marker=dict(
                sizemode="area",
                sizeref=max(df_map["GDP per capita"]) / 2000 if len(df_map) else 1
            )
        )

        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_colorbar=dict(title="Life Exp."),
        )

        st.plotly_chart(fig, use_container_width=True)
