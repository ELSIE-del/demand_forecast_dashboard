import pandas as pd

# Load the forecasted data
preview = pd.read_csv('./data/forecast_output.csv')
print("✅ Previewing forecasted demand with timestamps:")
print(preview.head())
