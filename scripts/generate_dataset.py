import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate 100 days of data
dates = [datetime.today() - timedelta(days=i) for i in range(100)]
dates.reverse()

# Simulate data
data = {
    'date': dates,
    'demand': np.random.randint(50, 500, size=100),
    'inventory_level': np.random.randint(100, 1000, size=100),
    'supplier_score': np.random.randint(40, 100, size=100),
    'delay_days': np.random.poisson(lam=2, size=100),
    'risk_flag': np.random.choice([0, 1], size=100, p=[0.85, 0.15])  # 1 = risky
}

df = pd.DataFrame(data)

# Save to CSV in the data folder
df.to_csv('../data/supply_chain_data.csv', index=False)

print("Sample dataset generated and saved to /data/supply_chain_data.csv")