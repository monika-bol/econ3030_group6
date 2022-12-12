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
yphhc = yphw/dfc['hc']

calc_table = pd.DataFrame(list(zip(dfc['country'], ypc, ypw, yphw, yphhc)), columns=['country','ypc', 'ypw', 'yphw', 'yphhc']).round(decimals=2)
print(calc_table.describe(percentiles = [0.95, 0.9, 0.1, 0.05]))

table = calc_table.quantile([1, 0.95, 0.9, 0.1, 0.05, 0])
def ratio(y):
    y_ratios = [round(table.iloc[0][y]/table.iloc[5][y]), round(table.iloc[1][y]/table.iloc[4][y]), round(table.iloc[2][y]/table.iloc[3][y])]
    return (y_ratios)

ratio_table = pd.DataFrame(list(zip(ratio('ypc'), ratio('ypw'), ratio('yphw'), ratio('yphhc'))), columns = ['ypc', 'ypw', 'yphw', 'yphhc'], index = ['rich/poor', '95/5', '90/10'] )
print(ratio_table)

def log_var(a):
    return(np.log(calc_table[a].var()))

log_var_table = pd.DataFrame(data = (log_var('ypc'), log_var('ypw'), log_var('yphw'), log_var('yphhc')), columns = ['log variance'], index = ['ypc', 'ypw', 'yphw', 'yphhc'])
print(log_var_table)

#4 (draft)
#find from ratio table that the disparity of standard of living (shown in ypc ratio) tends to get smaller
# once you take into account for yphw and then further as you account for yphhc
# especially at the most extreme ends of measures. 
# accounting for hours worked meant reduction by 1 unit, and a further 3 units once human capital (hc) per hour worked is considered


#5
x_axes = ypc, ypw, yphw, yphhc, ypw, ypc, ypw, yphw, yphhc, ypw, ypc, ypw, yphw, yphhc, ypw, ypc, ypw, yphw, yphhc, ypw, ypc, ypw, yphw, yphhc, ypw
y_axes = dfc.avh, dfc.avh, dfc.avh, dfc.avh, dfc.cn, dfc.cn, dfc.cn, dfc.cn, dfc.hc, dfc.hc, dfc.hc, dfc.hc, 1-dfc['labsh'], 1-dfc['labsh'], 1-dfc['labsh'], 1-dfc['labsh'], dfc.ctfp, dfc.ctfp, dfc.ctfp, dfc.ctfp
x_axes_labels = 'income per capita', 'income per worker', 'income per hour worked', 'income per hour human capital', 'income per capita', 'income per worker', 'income per hour worked', 'income per hour human capital', 'income per capita', 'income per worker', 'income per hour worked', 'income per hour human capital', 'income per capita', 'income per worker', 'income per hour worked', 'income per hour human capital', 'income per capita', 'income per worker', 'income per hour worked', 'income per hour human capital'
y_axes_labels = 'average anual hours worked', 'average anual hours worked', 'average anual hours worked', 'average anual hours worked', 'physical capital', 'physical capital', 'physical capital', 'physical capital', 'human capital', 'human capital', 'human capital', 'human capital', 'alpha', 'alpha', 'alpha', 'alpha', 'ctfp', 'ctfp', 'ctfp', 'ctfp' 
plt.figure(figsize=(10, 10))
plt.rcParams.update({'font.size': 5})
for i in range(0, 20):
    plt.subplot(5, 5, i+1)
    plt.scatter(np.log(x_axes[i]), y_axes[i], s = 2)
    plt.xlabel(x_axes_labels[i], fontsize = 5)
    plt.ylabel(y_axes_labels[i], fontsize = 5)
plt.tight_layout()
plt.show()
#need country code

#6 
ykh = np.power(dfc['cn'], (1-dfc['labsh']))*np.power((dfc['hc']/dfc['emp']),(dfc['labsh']))
ykh_ypc = ykh/dfc['pop']
ykh_ypw = ykh_ypc/dfc['emp']
ykh_yphw = ykh_ypw/dfc['avh']
ykh_yphhc = ykh_yphw/dfc['hc']

def success_1(y, ykh):
    var_log_y = (np.log([y])).var()
    var_log_ykh = (np.log([ykh])).var()
    return var_log_ykh/var_log_y

print('Using Y_kh...')
print('Success measure 1 for ypc: ', success_1 (ypc, ykh_ypc))
print('Success measure 1 for ypw: ', success_1 (ypw, ykh_ypw))
print('Success measure 1 for yphw: ', success_1(yphw, ykh_yphw))
print('Success measure 1 for yphhc: ', success_1(yphhc, ykh_yphhc))

#this is just to test which way round to do
print ((np.log(ypc)).var())
print (np.log(ypc.var()))

def success_2(y, ykh):


#7 
#are diffs in standards of livimg across countries mostly driven by factor accumulation
#or efficiency in factors used?

#do results depend on measure used?

#how does it differ from those in Caselli - 
#ANSWER We use a measure for 1-alpha being labsh, whereas Caselli uses a constant value of 0.666 for 1-alpha
#this means for caselli, the success measures are less than 1, whereas our results for success are larger than 1 

#8 
#As instructed in office hour, only need to compare the GDP per capita measure using TFP vs Y_kh
tfp = dfc['ctfp']/dfc['pop']
print('Using TFP...')
print('Success measure 1 for ypc: ', success_1(ypc, tfp))
print('Success measure 2 for ypc: ', success_2(,) )

# Find that the success measure is lower than when we use Y_kh, 
#meaning that (compare production factors impacts income differences more than productivity ??)
#need to compare to caselli 

#9
#think we need to make subsets for what part of dataset to use?