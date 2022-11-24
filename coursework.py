import pandas as pd
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/jivizcaino/PWT_10.0/main/pwt100.csv', encoding="latin-1")
df_subset = df[['country', 'year','pop', 'cgdpo', 'emp', 'avh', 'hc', 'labsh']]

#remove all entries that have NaN values 
#revisit this; probably better way of doing it
df_subset_cleaned=df_subset[~df_subset['avh'].isnull()]
df_subset_cleaned=df_subset_cleaned[~df_subset_cleaned['cgdpo'].isnull()]
df_subset_cleaned=df_subset_cleaned[~df_subset_cleaned['emp'].isnull()]
df_subset_cleaned=df_subset_cleaned[~df_subset_cleaned['hc'].isnull()]
df_subset_cleaned=df_subset_cleaned[~df_subset_cleaned['labsh'].isnull()]

group=df_subset_cleaned.groupby(['year'])
group=group.count()
print(group.idxmax(), group.query('2001'))
#the most recent year with the most observations is 2001, with 64