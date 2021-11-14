import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)

# transfer from csv to excel
# df_csv = pd.read_csv(r'E:\\Gybin\\athlete_events.csv')
# df_csv.to_excel(r'E:\\study\\Big_data\\athlete_events.xlsx', index=None, header=True)

df = pd.read_csv('E:\\Gybin\\athlete_events.csv')
df = df.drop_duplicates(keep='first')
print(df.info())
print(df.describe(include='all'))


# Youngest Athletes 1992
# Young_1992 = df.groupby(['Year', 'Sex'])\
#       .aggregate({'Age':'min'})
# print(Young_1992.loc[(1992)])

# Percent Basketball player on Olympic games
# Olympic_2012 = df.loc[df.Year == 2012].loc[df.Sex == 'M'].drop_duplicates(subset='Name', keep='first')
# Basket_percent = Olympic_2012.loc[df.Sport == 'Basketball'].drop_duplicates(subset='Name', keep='first')
# print(np.around(Basket_percent.shape[0]/Olympic_2012.loc[df.Sport != 'Basketball'].shape[0]*1000)/10)

# sem and std Tennis female in 2000 y.
# Olympic_2000 = df.loc[df.Year == 2000].loc[df.Sex == 'F'].loc[df.Sport == 'Tennis']
# print(f'Mean Height sportsmen female: {np.around((Olympic_2000.Height.sem())*10)/10}',
#       f'Std Height sportsmen female: {np.around(Olympic_2000.Height.std()*10)/10}', sep='\n')

# Search sportsmen top weight in 2006 y.
# heavyweight = df.loc[df.Year == 2006]
# print(heavyweight.loc[heavyweight.Weight == heavyweight.Weight.max()])

# How many times has John Aalberg participated
# print(f'John Aalberg participated in the Olympic Games:'
#       f' {df.loc[df.Name == "John Aalberg"].shape[0]} times')

# How many gold medals in tennis did Swiss athletes win at the 2008 Olympics
# Swiss_2000 = df.loc[df.Medal == 'Gold']\
#       .loc[df.Year == 2008]\
#       .loc[df.Sport == 'Tennis']\
#       .loc[df.NOC == 'SUI']
# print(Swiss_2000.shape[0])
# print(Swiss_2000.groupby(['Name'], as_index=False)\
#       .aggregate({'Medal':'count'}))

# Is it true that Spain won fewer medals than Italy at the 2016 Olympics? Medal = df.dropna(subset=['Medal']) if
# Medal.loc[Medal.NOC == 'ESP'].loc[Medal.Year == 2016].shape[0] > Medal.loc[Medal.NOC == 'ITA'].loc[Medal.Year ==
# 2016].shape[0]: print('No, the Spaniards have won more medals') elif Medal.loc[Medal.NOC == 'ESP'].loc[Medal.Year
# == 2016].shape[0] == Medal.loc[Medal.NOC == 'ITA'].loc[Medal.Year == 2016].shape[0]: print('The number of medals
# for both countries is the same') else: print('Yes it is, Spain won fewer medals than Italy at the 2016 Olympics')

# Which age group did the smallest and largest number of participants in the 2008 Olympic Games belong to?
# Age_group_2008 = df.loc[df.Year == 2008]
# print(Age_group_2008['Age'].value_counts(dropna=True))

# Is it true that the Summer Olympics were held in Atlanta? Is it true that Squaw Valley hosted the Winter Olympics?
print(df.loc[(df['City'] == 'Squaw Valley') | (df['City'] == 'Atlanta')]\
      .groupby(['City', 'Season'], as_index=False)\
      .aggregate({'Year': 'min'}))

# What is the absolute difference between the number of unique sports in the 1986 Olympics and the 2002 Olympics?
# uniq_1986 = df.loc[df.Year == 1986]
# uniq_2002 = df.loc[df.Year == 2002]
# print(abs(uniq_2002['Sport'].value_counts().shape[0]-uniq_1986['Sport'].value_counts().shape[0]))