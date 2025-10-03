import pandas as pd

# Load the dataset
df = pd.read_csv('../data/supply_chain_data.csv')

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Check for missing values
print("\n🔍 Missing Values:")
print(df.isnull().sum())

# Get basic statistics
print("\n📊 Summary Statistics:")
print(df.describe())

# Preview cleaned data
print("\n✅ Cleaned Data Preview:")
print(df.head())