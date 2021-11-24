import pandas as pd
import numpy as np
# test_git
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)

df = pd.read_csv('E:\\Gybin\\athlete_events.csv')
df.Medal.fillna('Nothing', inplace=True)
print('          Attributes and formats')
print(df.info())

des_stat_num = {'Name': ['ID', 'Age', 'Height', 'Weight'],
                'N': [df[i].dropna().shape[0] for i in ['ID', 'Age', 'Height', 'Weight']],
                'Min': [df[i].dropna().min() for i in ['ID', 'Age', 'Height', 'Weight']],
                'Max': [df[i].dropna().max() for i in ['ID', 'Age', 'Height', 'Weight']],
                'Mean': [df[i].dropna().mean() for i in ['ID', 'Age', 'Height', 'Weight']],
                'Missing': [df[i].isna().sum() for i in ['ID', 'Age', 'Height', 'Weight']],
                'Outliers': [df["ID"].quantile(.0)-1, df["Age"].quantile(.95),
                             df["Height"].quantile(.95), df["Weight"].quantile(.95)]}
df_num = pd.DataFrame(data=des_stat_num)
print('                    Descriptive statistic numbers')
print(df_num)

str_col = ['Name', 'Sex', 'Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal']
des_stat_char = {'Name': str_col,
                 'N': [df[i].shape[0] for i in str_col],
                 'Unique': [df[i].unique().shape[0] for i in str_col],
                 'Top': [df[i].value_counts(dropna=False).index[0] for i in str_col],
                 'Frequency': [df[i].value_counts(dropna=False).max() for i in str_col]}
df_char = pd.DataFrame(data=des_stat_char)
print('                 Descriptive statistic char')
print(df_char)


df = df.drop_duplicates(keep='first')
# Youngest Athletes 1992
Young_1992 = df.groupby(['Year', 'Sex'], as_index=False)\
      .aggregate({'Age': 'min'})
Young = (Young_1992.loc[Young_1992.Year == 1992])

# Percent Basketball player on Olympic games
Olympic_2012 = df.loc[df.Year == 2012].loc[df.Sex == 'M'].drop_duplicates(subset='Name', keep='first')
Basket_percent = Olympic_2012.loc[df.Sport == 'Basketball'].drop_duplicates(subset='Name', keep='first')
bas_per = np.around(Basket_percent.shape[0]/Olympic_2012.loc[df.Sport != 'Basketball'].shape[0]*1000)/10

# sem and std Tennis female in 2000 y.
Olympic_2000 = df.loc[df.Year == 2000].loc[df.Sex == 'F'].loc[df.Sport == 'Tennis']\
    .drop_duplicates(subset='Name', keep='first')
se_std = f'Sem: {np.around((Olympic_2000.Height.sem())*10)/10}'+' '+f'Std: {np.around(Olympic_2000.Height.std()*10)/10}'

# Search sportsmen top weight in 2006 y.
heavyweight = df.loc[df.Year == 2006]
fat = heavyweight.loc[heavyweight.Weight == heavyweight.Weight.max()]

# How many times has John Aalberg participated
john_aalberg = f'{df.loc[df.Name == "John Aalberg"].shape[0]} times'

# How many gold medals in tennis did Swiss athletes win at the 2008 Olympics
Swiss_2000 = df.loc[df.Medal == 'Gold']\
      .loc[df.Year == 2008]\
      .loc[df.Sport == 'Tennis']\
      .loc[df.NOC == 'SUI']
medal_count = Swiss_2000.groupby(['Name'], as_index=False)\
      .aggregate({'Medal': 'count'})

# Is it true that Spain won fewer medals than Italy at the 2016 Olympics?
Medal = df.dropna(subset=['Medal'])
if Medal.loc[Medal.NOC == 'ESP'].loc[Medal.Year == 2016].shape[0] \
        > Medal.loc[Medal.NOC == 'ITA'].loc[Medal.Year == 2016].shape[0]:
    rely = False
elif Medal.loc[Medal.NOC == 'ESP'].loc[Medal.Year == 2016].shape[0] \
        == Medal.loc[Medal.NOC == 'ITA'].loc[Medal.Year == 2016].shape[0]:
    rely = False
else:
    rely = True

# Which age group did the smallest and largest number of participants in the 2008 Olympic Games belong to?
Age_group_2008 = df.loc[df.Year == 2008]
Age_2008 = Age_group_2008['Age'].value_counts(dropna=True)

# Is it true that the Summer Olympics were held in Atlanta? Is it true that Squaw Valley hosted the Winter Olympics?
where = df.loc[(df['City'] == 'Squaw Valley') | (df['City'] == 'Atlanta')]\
      .groupby(['City', 'Season'], as_index=False)\
      .aggregate({'Year': 'min'})
if where.iloc[0, 1] == 'Summer':
    summer = True
else:
    summer = False
if where.iloc[1, 1] == 'Winter':
    winter = True
else:
    winter = False

# What is the absolute difference between the number of unique sports in the 1986 Olympics and the 2002 Olympics?
unique_86 = df.loc[df.Year == 1986]
unique_02 = df.loc[df.Year == 2002]
diff_abs = abs(unique_02['Sport'].value_counts().shape[0] - unique_86['Sport'].value_counts().shape[0])


# print('Question-Answer')
des_answer = {'Questing': range(1, 11),
              'Answer': [f'F: {Young.iloc[0, 2]} M: {Young.iloc[1, 2]}',
                         f'{bas_per} %',
                         se_std,
                         f'name: {fat.iloc[0, 1]}, weight: {fat.iloc[0, 5]}, sport: {fat.iloc[0, 12]}',
                         john_aalberg,
                         f'Medals: {Swiss_2000.shape[0]}. {medal_count.Name.iloc[0]} {medal_count.Medal.iloc[0]},'
                         f' {medal_count.Name.iloc[1]} {medal_count.Medal.iloc[1]}',
                         rely,
                         f'Age: {Age_2008.index[0]} - {Age_2008.iloc[0]},'
                         f' Age: {Age_2008.index[-1]} - {Age_2008.iloc[-1]},'
                         f' Age: {Age_2008.index[-2]} - {Age_2008.iloc[-2]}',
                         f'fact_Atlanta - {summer},'
                         f'fact_Squaw_Valley - {winter}',
                         diff_abs]}
df_answer_table = pd.DataFrame(data=des_answer)
print(df_answer_table.to_string(index=False))
