import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Demand Forecast Dashboard", layout="wide")

st.title("📊 Demand Forecast Dashboard")
st.markdown("Upload your forecast data and visualize trends, anomalies, and confidence intervals.")

with st.expander("🧭 How to Use This Dashboard"):
    st.markdown("""
    **Step 1:**Upload a CSV file with the following columns: 
                 - `date`: Timestamp of the forecast entry  
    - `demand`: Forecasted demand value  
    - `inventory_level`: Current inventory at that time  
    - `supplier_score`: Supplier reliability score  
    - `delay_days`: Delivery delay in days  
    - `risk_flag`: 1 if risky, 0 if safe  

    **Step 2:** Use the tabs to explore:
    - 📈 **Forecast**: View demand trends over time  
    - ⚠️ **Risk**: See red markers for flagged risks  
    - 📦 **Inventory**: Compare inventory vs demand  
    - 🗃️ **Raw Data**: Preview the uploaded dataset  

    **Step 3:** Click **Download CSV** to export your processed data
    """)
           
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
        st.subheader("Forecast Over Time with Confidence Interval")
        fig, ax = plt.subplots()
        ax.plot(df['Date'], df['Forecast'], label='Forecast', color='blue')
        
        # Confidence interval band (±20 units)
        lower_bound = df['Forecast'] - 20
        upper_bound = df['Forecast'] + 20
        ax.fill_between(df['Date'], lower_bound, upper_bound, color='blue', alpha=0.2, label='Confidence Interval')
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

