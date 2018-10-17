import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('./data.csv', index_col=0, parse_dates=True)
#print(df)

df2 = df[0].resample('T').sum() 
df2.head()

