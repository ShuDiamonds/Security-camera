import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DATE_FORMAT = "%Y_%m_%d %H:%M:%S"
my_date_parser = lambda d: pd.datetime.strptime(d, DATE_FORMAT)
df = pd.read_csv('./data.csv', index_col=0, date_parser=my_date_parser, names=["time","x","y"])
#print(df)
df["count"]=1


df2 = df.resample('60min',how='sum')
print(df.head())

