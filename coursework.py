import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('https://raw.githubusercontent.com/jivizcaino/PWT_10.0/main/pwt100.csv', encoding="latin-1")
df_subset = df[['country', 'countrycode', 'year', 'pop', 'cgdpo', 'emp', 'avh', 'hc', 'labsh', 'ctfp', 'cn']]
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
def ratio(y):
    y_ratios = [round(table.iloc[0][y]/table.iloc[5][y]), round(table.iloc[1][y]/table.iloc[4][y]), round(table.iloc[2][y]/table.iloc[3][y])]
    return (y_ratios)

ratio_table = pd.DataFrame(list(zip(ratio('ypc'), ratio('ypw'), ratio('yphw'), ratio('yphc'), ratio('yphhc'))), columns = ['ypc', 'ypw', 'yphw', 'yphc', 'yphhc'], index = ['rich/poor', '95/5', '90/10'] )
print(ratio_table)

def log_var(a):
    return(np.log(calc_table[a].var()))

log_var_table = pd.DataFrame(data = (log_var('ypc'), log_var('ypw'), log_var('yphw'), log_var('yphc'), log_var('yphhc')), columns = ['log variance'], index = ['ypc', 'ypw', 'yphw', 'yphc', 'yphhc'])
print(log_var_table)

#4

#5


plt.scatter(np.log(ypw), dfc.avh)
plt.show()

