import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('https://raw.githubusercontent.com/jivizcaino/PWT_10.0/main/pwt100.csv', encoding="latin-1")
df_subset = df[['country', 'countrycode', 'year', 'pop', 'cgdpo', 'emp', 'avh', 'hc', 'labsh', 'ctfp']]
df_subset = df_subset.query('year>=2010')

#remove entries with null values
dfc = df_subset.dropna()
print(dfc.describe())

group = dfc.groupby(['year'])
group = group.count()
print(group[::-1].idxmax())
#the most recent year with the most observations is 2019, with 61
dfc = dfc.query('year == 2019')

#3

ypc = dfc['cgdpo']/dfc['pop']
ypw = dfc['cgdpo']/dfc['emp']
yphw = ypw/dfc['avh']
yphc = dfc['cgdpo']/dfc['hc']
yphhc = yphw/dfc['hc']

calc_table = pd.DataFrame(columns=['country','ypc', 'ypw', 'yphw', 'yphc', 'yphhc'])
calc_table['country'] = dfc['country']
calc_table['ypc'] = ypc
calc_table['ypw'] = ypw
calc_table['yphw'] = yphw
calc_table['yphc'] = yphc
calc_table['yphhc'] = yphhc

calc_table = calc_table.round(decimals=2)
print(calc_table.describe(percentiles = [0.95, 0.9, 0.1, 0.05]))

table = calc_table.quantile([1, 0.95, 0.9, 0.1, 0.05, 0])
ypc_ratios = [round(table.iloc[0]['ypc']/table.iloc[5]['ypc']), round(table.iloc[1]['ypc']/table.iloc[4]['ypc']), round(table.iloc[2]['ypc']/table.iloc[3]['ypc'])]
ypw_ratios = [round(table.iloc[0]['ypw']/table.iloc[5]['ypw']), round(table.iloc[1]['ypw']/table.iloc[4]['ypw']), round(table.iloc[2]['ypw']/table.iloc[3]['ypw'])]
yphw_ratios = [round(table.iloc[0]['yphw']/table.iloc[5]['yphw']), round(table.iloc[1]['yphw']/table.iloc[4]['yphw']), round(table.iloc[2]['yphw']/table.iloc[3]['yphw'])]
yphc_ratios = [round(table.iloc[0]['yphc']/table.iloc[5]['yphc']), round(table.iloc[1]['yphc']/table.iloc[4]['yphc']), round(table.iloc[2]['yphc']/table.iloc[3]['yphc'])]
yphhc_ratios = [round(table.iloc[0]['yphhc']/table.iloc[5]['yphhc']), round(table.iloc[1]['yphhc']/table.iloc[4]['yphhc']), round(table.iloc[2]['yphhc']/table.iloc[3]['yphhc'])]

ratio_table = pd.DataFrame(list(zip(ypc_ratios, ypw_ratios, yphw_ratios, yphc_ratios, yphhc_ratios)), columns = ['ypc', 'ypw', 'yphw', 'yphc', 'yphhc'])
print(ratio_table)

#5


plt.scatter(np.log(ypw), dfc.avh)
plt.show()


#measures of success
