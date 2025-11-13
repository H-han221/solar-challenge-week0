import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(
    page_title="Solar Data Dashboard",
    page_icon="🌞",
    layout="wide"
)

st.title("🌞 Solar Data Dashboard")
st.markdown(
    "Explore and compare **solar radiation data** for **Benin**, **Togo**, and **Sierra Leone**."
)

# ----------------------------
# Load data
# ----------------------------
@st.cache_data
def load_data():
    data = {
        "Benin": pd.read_csv("data/benin_clean.csv"),
        "Togo": pd.read_csv("data/togo_clean.csv"),
        "Sierra Leone": pd.read_csv("data/sierraleone_clean.csv")
    }
    return data

data = load_data()

# ----------------------------
# Tabs
# ----------------------------
tabs = st.tabs(["🇧🇯 Benin", "🇹🇬 Togo", "🇸🇱 Sierra Leone", "📊 Summary Comparison"])

# ----------------------------
# Individual Country Tabs
# ----------------------------
for i, country in enumerate(["Benin", "Togo", "Sierra Leone"]):
    with tabs[i]:
        st.subheader(f"Solar Radiation in {country}")

        df = data[country]
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        if df.empty:
            st.warning(f"No data available for {country}. Check CSV file.")
        else:
            st.dataframe(df.head())
            if "date" in df.columns and "solar_radiation" in df.columns:
                fig, ax = plt.subplots()
                ax.plot(df["date"], df["solar_radiation"], label=country)
                ax.set_xlabel("Date")
                ax.set_ylabel("Solar Radiation (kWh/m²)")
                ax.legend()
                st.pyplot(fig)
            else:
                st.error("Missing 'date' or 'solar_radiation' columns.")

# ----------------------------
# Summary Comparison Tab
# ----------------------------
with tabs[3]:
    st.subheader("📊 Solar Radiation Summary Comparison")

    summary_data = []
    for country, df in data.items():
        if "solar_radiation" in df.columns:
            summary_data.append({
                "Country": country,
                "Average Radiation": round(df["solar_radiation"].mean(), 2),
                "Max Radiation": round(df["solar_radiation"].max(), 2),
                "Min Radiation": round(df["solar_radiation"].min(), 2)
            })

    summary_df = pd.DataFrame(summary_data)

    if not summary_df.empty:
        st.dataframe(summary_df)

        fig, ax = plt.subplots()
        ax.bar(summary_df["Country"], summary_df["Average Radiation"], color=["#ffb703", "#219ebc", "#8ecae6"])
        ax.set_ylabel("Average Solar Radiation (kWh/m²)")
        ax.set_title("Average Solar Radiation by Country")
        st.pyplot(fig)
    else:
        st.warning("No summary data available.")
