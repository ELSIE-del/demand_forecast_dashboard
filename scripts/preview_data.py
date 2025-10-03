import pandas as pd

# Load the dataset from the data folder
df = pd.read_csv('../data/supply_chain_data.csv')

# Show the first 5 rows
print("📊 Preview of Supply Chain Dataset:")
print(df.head())