import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

def train_model(df):
    X = df[['GDP per capita', 'headcount_ratio_upper_mid_income_povline', 'year']]
    y = df['Life Expectancy (IHME)']

    data = pd.concat([X, y], axis=1).dropna()
    X = data[['GDP per capita', 'headcount_ratio_upper_mid_income_povline', 'year']]
    y = data['Life Expectancy (IHME)']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)


    joblib.dump(model, "random_forest_model.pkl")



    feature_importance = dict(zip(X.columns, model.feature_importances_))
    return model, feature_importance
