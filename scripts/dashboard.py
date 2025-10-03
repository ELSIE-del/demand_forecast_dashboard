import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def classify_risk(d):
    if d > 450:
        return "High"
    elif d > 300:
        return "Moderate"
    else:
        return "Low"

# Load combined forecast data
df = pd.read_csv('./data/combined_output.csv')
df['date'] = pd.to_datetime(df['date'])
forecast_df = pd.DataFrame()

st.title("📦 Demand Forecast Dashboard")
tab1, tab2 = st.tabs(["📊 Forecast View", "📁 Upload & Retrain"])

with tab1:

# Convert pandas Timestamps to native python datetime 
 min_date = df['date'].min().to_pydatetime()
max_date = df['date'].max().to_pydatetime()

#Create the slider
date_range =  st.slider(
    "Select Date Range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

# Filter data by selected date range
filtered_df = df[
    (df['date'] >= pd.to_datetime(date_range[0])) & 
    (df['date'] <= pd.to_datetime(date_range[1]))
]

# Toggle actual vs forecast
show_actual = st.checkbox("Show Actual Demand",value=True)
show_forecast = st.checkbox("Show Forecasted Demand",value=True)

risk_colors = {'High': 'red', 'Moderate': 'orange', 'Low': 'green'}

fig, ax = plt.subplots(figsize=(10, 5))
if show_actual:
        ax.plot(filtered_df['date'], filtered_df['actual_demand'], label='Actual Demand', color='blue')



if show_forecast:
    ax.plot(filtered_df['date'], filtered_df['forecasted_demand'], label='Forecasted Demand', linestyle='--', color='orange')
   
    if not forecast_df.empty:
        ax.fill_between(forecast_df['date'], forecast_df['lower_bound'], forecast_df['upper_bound'],
                        color='orange', alpha=0.2, label='Confidence Interval')
# Highlight anomalies
if not forecast_df.empty and show_actual:
   anomalies = forecast_df[forecast_df['anomaly']]
   ax.scatter(anomalies['date'], anomalies['actual_demand'], color='black', marker='x', s=70, label='Anomaly')

if not forecast_df.empty and show_forecast:
    for _, row in forecast_df.iterrows():
        ax.scatter(row['date'], row['forecasted_demand'], color=risk_colors[row['risk_level']], s=50)

handles, labels = ax.get_legend_handles_labels()
unique = dict(zip(labels, handles))
ax.legend(unique.values(), unique.keys())

ax.set_xlabel("Date")
ax.set_ylabel("Demand")
ax.set_title("📈 Demand Forecast")
ax.grid(True)
st.pyplot(fig)

if not forecast_df.empty:
        st.subheader("📊 Risk Classification Table")
        st.dataframe(forecast_df[['date', 'forecasted_demand', 'risk_level']])
        st.download_button(
            label="📤 Download Forecast CSV",
            data=forecast_df.to_csv(index=False).encode('utf-8'),
            file_name='updated_forecast.csv',
            mime='text/csv'
        )
# Add anomaly table
if not forecast_df.empty and forecast_df['anomaly'].any():
    st.subheader("⚠️ Detected Anomalies")
    st.dataframe(forecast_df[forecast_df['anomaly']][['date', 'actual_demand', 'forecasted_demand', 'lower_bound', 'upper_bound']])

with tab2:
    
    uploaded_file = st.file_uploader("📁 Upload new demand CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df['date'] = pd.to_datetime(df['date']).dt.normalize()
        st.success("✅ New data loaded!")

    if st.button("🔄 Retrain Forecast Model"):
        from sklearn.linear_model import LinearRegression
        import numpy as np

        # Prepare training data
        df['day_index'] = np.arange(len(df))
        X = df[['day_index']]
        y = df['actual_demand'].dropna()

        # Train model
        model = LinearRegression()
        model.fit(X, y)

        y_pred = model.predict(X)
        error = np.std(y - y_pred)

        # Forecast next 30 days
        future_index = np.arange(len(df), len(df) + 30).reshape(-1, 1)
        forecast = model.predict(future_index)
        forecast_dates = pd.date_range(start=df['date'].max() + pd.Timedelta(days=1), periods=30).normalize()
        
        # Compute confidence bounds
        upper = forecast + error
        lower = forecast - error

        # Create forecast DataFrame
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'day_index': future_index.flatten(),
            'forecasted_demand': forecast,
            'upper_bound': upper,
            'lower_bound': lower,
            'actual_demand': None
        })

        # Add anomaly flag
        forecast_df['anomaly'] = (
            (forecast_df['actual_demand'].notna()) &
            ((forecast_df['actual_demand'] < forecast_df['lower_bound']) |
            (forecast_df['actual_demand'] > forecast_df['upper_bound']))
        )
        # Classify risk
        forecast_df['risk_level'] = forecast_df['forecasted_demand'].apply(classify_risk)

        # Merge with main DataFrame
        df = pd.concat([df, forecast_df], ignore_index=True)
        st.success("✅ Forecast updated!")

