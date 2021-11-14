import pandas as pd
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pylab as plt

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)

df = pd.read_csv('E:\\Gybin\\athlete_events.csv')
df.Medal.fillna('Nothing', inplace=True)
df = df.drop_duplicates(keep='first')


# Input data
# event, sport, sex = input('Input event for the predicted: '),
# input('Input sport for the predicted: '),
# input('Input sex for the predicted: ')
event, sport, sex = "Biathlon Men's 20 kilometres", "Biathlon", "M"


# check all rows on nan
def chek_nun():
    if .5 < prim_select.value_counts(dropna=True).shape[0] / prim_select.value_counts(dropna=False).shape[0] < .95:
        return prim_select.fillna((prim_select.mean(numeric_only=True)))
    elif .95 < prim_select.value_counts(dropna=True).shape[0] / prim_select.value_counts(dropna=False).shape[0]:
        return prim_select.dropna()
    else:
        if prim_select.Height.value_counts(dropna=True).shape[0] / prim_select.value_counts(dropna=False).shape[0] < .5:
            return prim_select.drop('Height', axis=1)
        elif prim_select.Weight.value_counts(dropna=True).shape[0] / prim_select.value_counts(dropna=False).shape[0] \
                < .5:
            return prim_select.drop('Weight', axis=1)
        elif prim_select.Age.value_counts(dropna=True).shape[0] / prim_select.value_counts(dropna=False).shape[0] < .5:
            return prim_select.drop('Age', axis=1)


# linear regression
def predict(name_parameter):
    parameter = sec_select[['Year', name_parameter]]
    parameter = parameter.astype({"Year": float})
    X = parameter.iloc[:, :-1].values
    y = parameter.iloc[:, 1].values
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.13, random_state=13)
    regress = LinearRegression()
    regress.fit(X_train, Y_train)
    y_pre = regress.predict(X_test)
    return y_pre


#  plot predict
def plot(parameter_):
    if parameter_ == 'Height':
        k = .01
    elif parameter_ == 'Weight':
        k = .03
    else:
        k = .05
    parameter = sec_select[['Year', parameter_]]
    parameter = parameter.assign(Low_predict=parameter.iloc[:, 1].values, High_predict=parameter.iloc[:, 1].values)
    parameter = parameter.append([{'Year': 2014}, {'Year': 2018}], ignore_index=True).replace(
        {parameter_: {np.nan: predict(parameter_)},
         'Low_predict': {np.nan: (1-k)*predict(parameter_)},
         'High_predict': {np.nan: (1+k)*predict(parameter_)}})
    print(parameter)
    parameter = parameter.astype({"Year": float})
    parameter.index = parameter['Year']
    plt.plot(parameter['Low_predict'], label='Year(X)')
    plt.plot(parameter['High_predict'], label='Year(X)')
    plt.plot(parameter[parameter_], label='Year(X)')
    plt.show()


# Prepared
prim_select = df.loc[(df.Sport == sport) & (df.Event == event) & (df.Medal == 'Gold')].sort_values(by=['Year'])
sec_select = chek_nun()
sec_select = sec_select[:-1]

# Regression analysis, predict and plot
result = smf.ols(formula="Weight ~ Year", data=sec_select).fit()
# print(result.summary())
print(f'Predicted for two years by weight: {predict("Weight")}')
plot('Weight')
#
# result = smf.ols(formula="Height ~ Year", data=sec_select).fit()
# print(result.summary())
print(f'Predicted for two years by height: {predict("Height")}')
plot('Height')
#
# result = smf.ols(formula="Age ~ Year", data=sec_select).fit()
# print(result.summary())
print(f'Predicted for two years by age: {predict("Age")}')
plot('Age')
