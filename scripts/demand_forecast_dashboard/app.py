import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Demand Forecast Dashboard", layout="wide")

st.title("📊 Demand Forecast Dashboard")
st.markdown("Upload your forecast data and visualize trends, anomalies, and confidence intervals.")

# File uploader
uploaded_file = st.file_uploader("Upload your forecast CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    # Rename columns to match expected format
    df.rename(columns={'date': 'Date', 'demand': 'Forecast'}, inplace=True)

    # Basic plot
    if 'Date' in df.columns and 'Forecast' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        fig, ax = plt.subplots()
        ax.plot(df['Date'], df['Forecast'], label='Forecast')
        
        # Overlay risk points
        risk_points = df[df['risk_flag'] == 1]
        ax.scatter(risky_points['Date'], risky_points['Forecast'], color='red',label='Risk', zorder = 5)
        
        ax.set_title("Forecast Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Forecast")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Make sure your CSV has 'Date' and 'Forecast' columns.")
else:
    st.info("Awaiting CSV upload...")

