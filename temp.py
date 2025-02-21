import pandas as pd

df=pd.read_csv("temp.csv")
#print(df['PlayerName'].apply(lambda x: x.split()[-1]))
print(df['PlayerName'].apply(type).value_counts())
