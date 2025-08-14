import streamlit as st
import pandas as pd
import numpy as np
from model import train_model
import matplotlib.pyplot as plt
import joblib


# --- Load dataset ---
url = "https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv"
df = pd.read_csv(url)
df.columns = df.columns.str.strip()
df['Life Expectancy (IHME)'] = pd.to_numeric(df['Life Expectancy (IHME)'], errors='coerce')
df['GDP per capita'] = pd.to_numeric(df['GDP per capita'], errors='coerce')
df['headcount_ratio_upper_mid_income_povline'] = pd.to_numeric(
    df['headcount_ratio_upper_mid_income_povline'], errors='coerce'
)

# --- Page layout ---
st.set_page_config(layout="wide")
st.title("Worldwide Analysis of Quality of Life and Economic Factors")

tab1, tab2, tab3 = st.tabs(["Global Overview", "Country Deep Dive", "Data Explorer"])

# =====================
# Tab 1: Global Overview
# =====================
with tab1:
    st.write("### Global Overview")

    year_selected = st.slider(
        "Select Year",
        min_value=int(df["year"].min()),
        max_value=int(df["year"].max()),
        value=int(df["year"].min())
    )
    df_year = df[df["year"] == year_selected]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        mean_life_exp = df_year["Life Expectancy (IHME)"].mean()
        st.metric("Mean Life Expectancy", f"{mean_life_exp:.2f}", "Average years people live")

    with col2:
        median_gdp = df_year["GDP per capita"].median()
        st.metric("Median GDP per Capita", f"${median_gdp:,.0f}", "Middle value of GDP per person")

    with col3:
        mean_poverty = df_year["headcount_ratio_upper_mid_income_povline"].mean()
        st.metric("Mean Poverty Rate", f"{mean_poverty:.2f}%", "Average % living under poverty line")

    with col4:
        num_countries = df_year["country"].nunique()
        st.metric("Number of Countries", num_countries, "Countries reporting data")

    st.write("---")

    # --- Task 6: Simple RandomForest model ---
    st.write("### Task 6: Predict Life Expectancy")

    # Train model
    ###model, feature_importance = train_model(df)

    # Create input fields
    gdp_input = st.number_input(
        "GDP per capita", 
        min_value=float(df['GDP per capita'].min()), 
        max_value=float(df['GDP per capita'].max()), 
        value=float(df['GDP per capita'].median())
    )
    poverty_input = st.number_input(
        "Upper-middle-income Poverty Rate (%)", 
        min_value=float(df['headcount_ratio_upper_mid_income_povline'].min()), 
        max_value=float(df['headcount_ratio_upper_mid_income_povline'].max()), 
        value=float(df['headcount_ratio_upper_mid_income_povline'].median())
    )
    year_input = st.number_input(
        "Year", 
        min_value=int(df['year'].min()),
        max_value=int(df['year'].max()), 
        value=int(df['year'].median())
    )
gdp_input = st.number_input("GDP per capita")
poverty_input = st.number_input("Upper-middle-income Poverty Rate (%)")
year_input = st.number_input("Year")
    # Load saved model

@st.cache_resource
def load_model():
    return joblib.load("random_forest_model.pkl")

model_trained = load_model()


if st.button("Predict Life Expectancy"):
    X_new = np.array([[gdp_input, poverty_input, year_input]])
    prediction = model_trained.predict(X_new)[0]
    st.success(f"Predicted Life Expectancy: {prediction:.2f} years")

    # Feature importance plot
    st.write("#### Feature Importance")
    fig, ax = plt.subplots()
    ax.bar(feature_importance.keys(), feature_importance.values())
    ax.set_ylabel("Importance")
    ax.set_title("RandomForest Feature Importance")
    st.pyplot(fig)

