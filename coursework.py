import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('https://raw.githubusercontent.com/jivizcaino/PWT_10.0/main/pwt100.csv', encoding="latin-1")
df_subset = df[['country', 'year', 'pop', 'cgdpo', 'emp', 'avh', 'hc', 'labsh']]
df_subset = df_subset.query('year>=2010')

#remove entries with null values
dfc = df_subset.dropna()

group = dfc.groupby(['year'])
group = group.count()
print(group[::-1].idxmax())
#the most recent year with the most observations is 2019, with 61
dfc = dfc.query('year == 2019')