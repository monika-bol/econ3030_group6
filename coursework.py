import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('https://raw.githubusercontent.com/jivizcaino/PWT_10.0/main/pwt100.csv', encoding="latin-1")
df_subset = df[['country', 'countrycode', 'year', 'pop', 'cgdpo', 'emp', 'avh', 'hc', 'labsh', 'ctfp', 'cn']]
df_subset = df_subset.query('year>=2010')

#remove entries with null values
dfc = df_subset.dropna()
print(dfc.describe().round(decimals=2))

group = dfc.groupby(['year'])
group = group.count()
print(group[::-1].idxmax())
#the most recent year with the most observations is 2019, with 61
dfc = dfc.query('year == 2019')
dfc_original = dfc
#3

ypc = dfc['cgdpo']/dfc['pop']
ypw = dfc['cgdpo']/dfc['emp']
yphw = ypw/dfc['avh']
yphhc = yphw/dfc['hc']

calc_table = pd.DataFrame(list(zip(dfc['country'], ypc, ypw, yphw, yphhc)), columns=['country','ypc', 'ypw', 'yphw', 'yphhc']).round(decimals=2)
print(calc_table.describe(percentiles = [0.95, 0.9, 0.1, 0.05]).round(decimals=2))

table = calc_table.quantile([1, 0.95, 0.9, 0.1, 0.05, 0])
def ratio(y):
    y_ratios = [round(table.iloc[0][y]/table.iloc[5][y]), round(table.iloc[1][y]/table.iloc[4][y]), round(table.iloc[2][y]/table.iloc[3][y])]
    return (y_ratios)

ratio_table = pd.DataFrame(list(zip(ratio('ypc'), ratio('ypw'), ratio('yphw'), ratio('yphhc'))), columns = ['ypc', 'ypw', 'yphw', 'yphhc'], index = ['rich/poor', '95/5', '90/10'] )
print(ratio_table)

def log_var(a):
    return((np.log(calc_table[a])).var())
    

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
colours = 'red', 'red', 'red', 'red', 'blue', 'blue', 'blue', 'blue', 'yellow', 'yellow', 'yellow', 'yellow', 'green', 'green', 'green', 'green', 'orange', 'orange', 'orange', 'orange'
plt.figure(figsize=(10, 10))
plt.rcParams.update({'font.size':3})
for i in range(0, 20):
    plt.subplot(5, 4, i+1)
    plt.scatter(np.log(x_axes[i]), y_axes[i], s = 2, color = colours[i])
    plt.xlabel(x_axes_labels[i], fontsize = 5)
    plt.ylabel(y_axes_labels[i], fontsize = 5)
    for a, txt in enumerate(dfc.countrycode):
        plt.annotate(txt, (np.log(x_axes[i].reset_index()[0][a]), y_axes[i].reset_index(drop = True)[a]))
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


def success_2(y, ykh, u, l):
    ykh_u = ykh.quantile([u])[u]
    ykh_l = ykh.quantile([l])[l]
    y_u = y.quantile([u])[u]
    y_l = y.quantile([l])[l]
    return (ykh_u/ykh_l)/(y_u/y_l)

success_2_table = pd.DataFrame(data = ([success_2(ypc, ykh_ypc, 0.9, 0.1), success_2(ypc, ykh_ypc, 0.99, 0.01), success_2(ypc, ykh_ypc, 0.95, 0.05), success_2(ypc, ykh_ypc, 0.75, 0.25)], [success_2(ypw, ykh_ypw, 0.9, 0.1), success_2(ypw, ykh_ypw, 0.99, 0.01), success_2(ypw, ykh_ypw, 0.95, 0.05), success_2(ypw, ykh_ypw, 0.75, 0.25)], [success_2(yphw, ykh_yphw, 0.9, 0.1), success_2(yphw, ykh_yphw, 0.99, 0.01), success_2(yphw, ykh_yphw, 0.95, 0.05), success_2(yphw, ykh_yphw, 0.75, 0.25)], [success_2(yphhc, ykh_yphhc, 0.9, 0.1), success_2(yphhc, ykh_yphhc, 0.99, 0.01), success_2(yphhc, ykh_yphhc, 0.95, 0.05), success_2(yphhc, ykh_yphhc, 0.75, 0.25)]), columns = ['90th-10th', '99th-1st', '95th-5th', '75th-25th'], index = ['ypc', 'ypw', 'yphw', 'yphhc'])
                    
print(success_2_table.round(decimals = 2))

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
print('Success measure 2 for ypc for the 90th and 10th percentile: ', success_2(ypc, tfp, 0.9, 0.1))

# Find that the success measure is lower than when we use Y_kh, 
#meaning that (compare production factors impacts income differences more than productivity ??)
#need to compare to caselli 

#9
#think we need to make subsets for what part of dataset to use?#think we need to make subsets for what part of dataset to use?
dfc['ypc'] = ypc
europe_list = ['Estonia', 'Slovenia', 'Czech Republic', 'Malta', 'Spain', 'Italy', 'France', 'United Kingdom', 'Finland', 'Belgium', 'Germany', 'Sweden', 'Austria', 'Iceland', 'Denmark', 'Netherlands' 'Norway', 'Switzerland', 'Luxembourg', 'Ireland', 'Lithuania', 'Cyprus', 'Poland', 'Portugal', 'Latvia', 'Hungary', 'Russian Federation', 'Romania', 'Slovakia', 'Greece', 'Croatia', 'Bulgaria']
asia_oceania_list = ['Israel', 'India', 'Philippines', 'Indonesia', 'Sri Lanka', 'China', 'Thailand', 'Malaysia', 'Japan', 'Republic of Korea', 'Taiwan', 'China, Hong Kong SAR', 'Singapore', 'Australia', 'New Zealand']
americas_list = ['Ecuador', 'Peru', 'Colombia', 'Brazil', 'Dominican Republic', 'Costa Rica', 'Mexico', 'Uruguay', 'Argentina', 'Chile', 'Canada', 'United States']
above_median = dfc.sort_values('ypc').reset_index(drop=True).query('index>30')
above_median_list = above_median.country.tolist()
below_median = dfc.sort_values('ypc').reset_index(drop=True).query('index<=30')
below_median_list = below_median.country.tolist()
OECD_countries_list = ['Australia', 'Austria', 'Belgium', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Israel', 'Italy', 'Japan', 'Korea', 'Latvia', 'Lithuania', 'Luxembourg', 'Mexico', 'Netherlands', 'New Zealand', 'Norway', 'Poland', 'Portugal', 'Slovak Republic', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'United Kingdom', 'United States']
non_OECD_countries_list = ['Singapore', 'Malta', 'Tawian', 'China', 'India', 'Philippines', 'Ecuador', 'Indonesia', 'Peru', 'South Africa', 'Sri Lanka', 'Brazil', 'Thailand', 'Dominican Republic', 'Costa Rica', 'Uruguay', 'Bulgaria', 'Argentina', 'Malaysia', 'Croatia', 'Romania', 'Russian Federation', 'Cyprus']

different_subsets = europe_list, asia_oceania_list, americas_list, above_median_list, below_median_list, OECD_countries_list, non_OECD_countries_list
subsets_names = "europe", "asia", "americas", "countries above median", "countries below median", "oecd countries", "non-oecd countries"

for n, i in enumerate(different_subsets):
    print("results for", subsets_names[n])
    dfc = dfc[dfc['country'].isin(i)]
    ypc = dfc['cgdpo']/dfc['pop']
    ypw = dfc['cgdpo']/dfc['emp']
    yphw = ypw/dfc['avh']
    yphhc = yphw/dfc['hc']
    
    calc_table = pd.DataFrame(list(zip(dfc['country'], ypc, ypw, yphw, yphhc)), columns=['country','ypc', 'ypw', 'yphw', 'yphhc']).round(decimals=2)
    ykh = np.power(dfc['cn'], (1-dfc['labsh']))*np.power((dfc['hc']/dfc['emp']),(dfc['labsh']))
    ykh_ypc = ykh/dfc['pop']
    ykh_ypw = ykh_ypc/dfc['emp']
    ykh_yphw = ykh_ypw/dfc['avh']
    ykh_yphhc = ykh_yphw/dfc['hc']

    print('Using Y_kh...')
    print('Success measure 1 for ypc: ', success_1 (ypc, ykh_ypc))
    print('Success measure 1 for ypw: ', success_1 (ypw, ykh_ypw))
    print('Success measure 1 for yphw: ', success_1(yphw, ykh_yphw))
    print('Success measure 1 for yphhc: ', success_1(yphhc, ykh_yphhc))

    success_2_table = pd.DataFrame(data = ([success_2(ypc, ykh_ypc, 0.9, 0.1), success_2(ypc, ykh_ypc, 0.99, 0.01), success_2(ypc, ykh_ypc, 0.95, 0.05), success_2(ypc, ykh_ypc, 0.75, 0.25)], [success_2(ypw, ykh_ypw, 0.9, 0.1), success_2(ypw, ykh_ypw, 0.99, 0.01), success_2(ypw, ykh_ypw, 0.95, 0.05), success_2(ypw, ykh_ypw, 0.75, 0.25)], [success_2(yphw, ykh_yphw, 0.9, 0.1), success_2(yphw, ykh_yphw, 0.99, 0.01), success_2(yphw, ykh_yphw, 0.95, 0.05), success_2(yphw, ykh_yphw, 0.75, 0.25)], [success_2(yphhc, ykh_yphhc, 0.9, 0.1), success_2(yphhc, ykh_yphhc, 0.99, 0.01), success_2(yphhc, ykh_yphhc, 0.95, 0.05), success_2(yphhc, ykh_yphhc, 0.75, 0.25)]), columns = ['90th-10th', '99th-1st', '95th-5th', '75th-25th'], index = ['ypc', 'ypw', 'yphw', 'yphhc'])
                    
    print(success_2_table.round(decimals = 2))
    dfc = dfc_original