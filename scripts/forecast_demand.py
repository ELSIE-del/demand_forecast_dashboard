import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('./data/supply_chain_data.csv')
df['date'] = pd.to_datetime(df['date'])

# Create a time index for modeling
df['day_index'] = np.arange(len(df))

# Prepare features and target
X = df[['day_index']]
y = df['demand']

# Train the model
model = LinearRegression()
model.fit(X, y)

# Forecast next 30 days
future_index = np.arange(len(df), len(df) + 30).reshape(-1, 1)
forecast = model.predict(future_index)

# Generate future dates starting from the last date in the dataset
last_date = df['date'].iloc[-1]
forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=30)

#Keep only the date part (drop hours/minutes/seconds)
forecast_dates = forecast_dates.normalize()

#Save forecast to CSV
forecast_df = pd.DataFrame({
    'date': forecast_dates,
    'day_index': future_index.flatten(),
    'forecasted_demand': forecast
})

forecast_df.to_csv('./data/forecast_output.csv', index=False)

# Combine actual and forecast into one timeline
actual_df = df[['date', 'day_index', 'demand']].copy()
actual_df.rename(columns={'demand': 'actual_demand'}, inplace=True)

# Add a placeholder column for forecast in the actual data
actual_df['forecasted_demand'] = None

# Align forecast with actual
forecast_df['actual_demand'] = None

# Merge them together
combined_df = pd.concat([actual_df, forecast_df], ignore_index=True)
combined_df.to_csv('./data/combined_output.csv', index=False)

# Plot results
plt.figure(figsize=(10, 5))
plt.plot(df['date'], df['demand'], label='Actual Demand',color = 'blue')
plt.plot(forecast_df['date'], forecast_df['forecasted_demand'], label='Forecasted Demand', linestyle='--', color='orange')

# Add vertical line at forecast start
forecast_start = forecast_df['date'].iloc[0]
plt.axvline(x=forecast_start,color = 'red',linestyle = ':',label = 'Forecast start')

plt.xlabel('Date')
plt.ylabel('Demand')
plt.title('📈 Demand Forecast (Next 30 Days)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# preview the saved forecast
preview = pd.read_csv('./data/forecast_output.csv')
print("✅Previewing forecasted demand with timestamps:")
print(preview.head())