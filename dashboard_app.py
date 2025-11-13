# ===============================
# Solar Data Dashboard (Final + Bonus)
# Author: Hanan Bedru
# ===============================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title="Solar Data Dashboard", page_icon="☀️", layout="wide")

st.title("☀️ Solar Data Dashboard")
st.markdown("""
Explore and compare **solar radiation data** for  
**Benin**, **Togo**, and **Sierra Leone**.
""")

# -------------------------------
# LOAD DATA FUNCTION
# -------------------------------
@st.cache_data
def load_data(country):
    path = f"data/{country}_clean.csv"
    return pd.read_csv(path)

# -------------------------------
# COUNTRY TABS + SUMMARY TAB
# -------------------------------
tabs = st.tabs(["🇧🇯 Benin", "🇹🇬 Togo", "🇸🇱 Sierra Leone", "📈 Summary Comparison"])

countries = ["benin", "togo", "sierra_leone"]
data_dict = {}

for i, country in enumerate(countries):
    with tabs[i]:
        st.subheader(f"📊 {country.capitalize()} Solar Data Overview")

        try:
            df = load_data(country)
            data_dict[country] = df  # store for summary tab
        except FileNotFoundError:
            st.error(f"❌ Missing file: data/{country}_clean.csv")
            continue

        st.write("### Data Preview")
        st.dataframe(df.head())

        # Summary statistics
        st.write("### Summary Statistics")
        st.write(df.describe())

        # Numeric columns
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        selected_col = st.selectbox(f"Select column to visualize ({country})", numeric_cols)

        # Line chart
        st.write(f"### {selected_col} Trend Over Time")
        fig, ax = plt.subplots(figsize=(8, 4))
        if 'Timestamp' in df.columns:
            ax.plot(df['Timestamp'], df[selected_col], label=selected_col, color='orange')
            ax.set_xlabel("Timestamp")
        else:
            ax.plot(df[selected_col], color='orange')
            ax.set_xlabel("Index")
        ax.set_ylabel(selected_col)
        ax.set_title(f"{selected_col} over time in {country.capitalize()}")
        st.pyplot(fig)

        # Correlation heatmap
        st.write("### Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

        # Distribution plots
        st.write("### Distribution of Key Variables")
        selected_cols = st.multiselect(f"Select variables for histogram ({country})", numeric_cols, default=numeric_cols[:2])
        for col in selected_cols:
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            ax.set_title(f"Distribution of {col}")
            st.pyplot(fig)

# -------------------------------
# BONUS TAB: Summary Comparison
# -------------------------------
with tabs[3]:
    st.subheader("🌍 Country Comparison Summary")

    # Only run if all data are loaded
    if all(c in data_dict for c in countries):
        summary_df = pd.DataFrame({
            "Country": [c.capitalize() for c in countries],
            "Mean GHI": [data_dict[c]["GHI"].mean() for c in countries],
            "Mean DNI": [data_dict[c]["DNI"].mean() for c in countries],
            "Mean DHI": [data_dict[c]["DHI"].mean() for c in countries]
        })

        st.write("### Average Solar Irradiance by Country")
        st.dataframe(summary_df)

        # Bar plot comparison
        st.write("### 📊 Comparison of Solar Metrics")
        melted = summary_df.melt(id_vars="Country", var_name="Metric", value_name="Value")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x="Country", y="Value", hue="Metric", data=melted, ax=ax)
        ax.set_title("Comparison of GHI, DNI, DHI across Countries")
        st.pyplot(fig)

        # Highlight best performer
        best_country = summary_df.loc[summary_df["Mean GHI"].idxmax(), "Country"]
        st.success(f"🏆 **{best_country}** has the highest average GHI (solar potential).")
    else:
        st.warning("Please ensure all 3 cleaned datasets (benin, togo, sierra_leone) are in the data/ folder.")

st.success("Dashboard loaded successfully!")
