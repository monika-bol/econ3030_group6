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

#5

plt.subplot(5,5,1)
plt.scatter(np.log(ypw), dfc.avh)

plt.subplot(5,5,2)
plt.scatter(np.log(ypw), dfc.cn)

plt.subplot(5,5,3)
plt.scatter(np.log(ypw), dfc.hc)

plt.subplot(5,5,4)
plt.scatter(np.log(ypw), 1-dfc['labsh'])

plt.subplot(5,5,5)
plt.scatter(np.log(ypw), dfc.ctfp)

plt.subplot(5,5,6)
plt.scatter(np.log(yphw), dfc.avh)

plt.subplot(5,5,7)
plt.scatter(np.log(yphw), dfc.cn)

plt.subplot(5,5,8)
plt.scatter(np.log(yphw), dfc.hc)

plt.subplot(5,5,9)
plt.scatter(np.log(yphw), 1-dfc['labsh'])

plt.subplot(5,5,10)
plt.scatter(np.log(yphw), dfc.ctfp)

plt.subplot(5,5,11)
plt.scatter(np.log(yphc), dfc.avh)

plt.subplot(5,5,12)
plt.scatter(np.log(yphc), dfc.cn)

plt.subplot(5,5,13)
plt.scatter(np.log(yphc), dfc.hc)

plt.subplot(5,5,14)
plt.scatter(np.log(yphc), 1-dfc['labsh'])

plt.subplot(5,5,15)
plt.scatter(np.log(yphc), dfc.ctfp)

plt.subplot(5,5,16)
plt.scatter(np.log(yphhc), dfc.avh)

plt.subplot(5,5,17)
plt.scatter(np.log(yphhc), dfc.cn)

plt.subplot(5,5,18)
plt.scatter(np.log(yphhc), dfc.hc)

plt.subplot(5,5,19)
plt.scatter(np.log(yphhc), 1-dfc['labsh'])

plt.subplot(5,5,20)
plt.scatter(np.log(yphhc), dfc.ctfp)

plt.subplot(5,5,21)
plt.scatter(np.log(ypc), dfc.avh)

plt.subplot(5,5,22)
plt.scatter(np.log(ypc), dfc.cn)

plt.subplot(5,5,23)
plt.scatter(np.log(ypc), dfc.hc)

plt.subplot(5,5,24)
plt.scatter(np.log(ypc), 1-dfc['labsh'])

plt.subplot(5,5,25)
plt.scatter(np.log(ypc), dfc.ctfp)

plt.show()
#measures of success

