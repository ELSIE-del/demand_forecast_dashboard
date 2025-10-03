import pandas as pd

df = pd.read_csv('./data/combined_output.csv')
print("✅ Loaded combined_output.csv")
print(df.tail(10))