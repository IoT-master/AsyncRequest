import pandas as pd

df = pd.read_json('./AMDFullOptionChain.json')
print(df.head())
print(df.columns)
df.plot('strike_price', 'implied_volatility')