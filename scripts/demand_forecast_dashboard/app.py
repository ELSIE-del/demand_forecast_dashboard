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
    
    # Rename columns to match expected format
    df.rename(columns={'date': 'Date', 'demand': 'Forecast'}, inplace=True)

    # Basic plot
    df['Date'] = pd.to_datetime(df['Date'])
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Forecast", "⚠️ Risk", "📦 Inventory", "🗃️ Raw Data"])
       
    with tab1:
        st.subheader("Forecast Over Time")
        fig, ax = plt.subplots()
        ax.plot(df['Date'], df['Forecast'], label='Forecast', color='blue')
        ax.set_title("Forecast Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Forecast")
        ax.legend()
        st.pyplot(fig)

    with tab2:
        st.subheader("Risk Overlay")
        fig, ax = plt.subplots()
        ax.plot(df['Date'], df['Forecast'], label='Forecast', color='blue')
        risk_points = df[df['risk_flag'] == 1]    
        ax.scatter(risk_points['Date'], risk_points['Forecast'], color='red',label='Risk', zorder=5)
        ax.set_title("Risk-Flagged Forecast")    
        ax.set_xlabel("Date")
        ax.set_ylabel("Forecast")
        ax.legend()
        st.pyplot(fig)

    with tab3:
        st.subheader("Inventory vs Forecast")
        fig, ax = plt.subplots()
        ax.plot(df['Date'], df['Forecast'], label='Forecast', color='blue')
        ax.plot(df['Date'], df['inventory_level'], label='Inventory Level', color='green')
        ax.set_title("Inventory vs Forecast")
        ax.set_xlabel("Date")
        ax.set_ylabel("Value")
        ax.legend()
        st.pyplot(fig)

    with tab4:
        st.subheader("Preview of Uploaded Data")
        st.dataframe(df.head())

    # Download button (outside tabs so it's always visible)
    st.subheader("Download Forecast Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="forecast_with_risk.csv",
        mime="text/csv"

        )               
    

else:
        st.info("Awaiting CSV upload...")

