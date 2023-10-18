# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 15:49:40 2023

@author: polya
"""

import os
os.chdir("d:/Nastya/маг2/анализ данных/lab/work_git/dataAnalize/work/")
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy as sc
import seaborn as sb
from collections import Counter

pth_b = './data/Salaries.xlsx'
CARSB = pd.read_excel(pth_b)

def analizeQuantitiveVariable(data):
    print("    Минимум:", data.min())
    print("    Максимум:", data.max())
    print("    Среднее:", np.mean(data))
    print("    Медиана:", np.median(data))
    print("    Среднеквадратическое отклонение:", np.std(data))
    print("    Коэффициент вариации:", np.var(data))
    print("    Асимметрия:", sc.stats.skew(data))
    print("    Эксцесс:", sc.stats.kurtosis(data))
    print("    Процентиль 5%:", np.percentile(data, 5))
    print("    Процентиль 95%:", np.percentile(data, 95))
    print("    Межквартильный размах (Interquartile range):", sc.stats.iqr(data))

CB = CARSB.copy()
CB = CB.astype({'Age':np.float64, 'Gender':'category', 'City':'category', 'Position':'category',
                'Total_years_of_experience':np.float64, 'Seniority_level':'category', 
                'Salary':np.float64})

from pandas.api.types import CategoricalDtype
cat_type_gender = CategoricalDtype(categories=["Male", "Female"], ordered=False)
CB['Gender'] = CB['Gender'].astype(cat_type_gender)

# Анализ колличественных переменных
print("Анализ количественных переменных\n")
print("Возраст:")
analizeQuantitiveVariable(CB['Age'])
print("Опыт работы:")
analizeQuantitiveVariable(CB['Total_years_of_experience'])
print("Заработная плата:")
analizeQuantitiveVariable(CB['Salary'])

# Графики гистограммы совместно с графиком плотности нормального распределения
sb.distplot(CB['Age'], hist=True, kde=True, 
             color = 'darkblue', 
             hist_kws={'edgecolor':'black'}).set_title('Распределение возраста')
sb.distplot(CB['Total_years_of_experience'], hist=True, 
            kde=True, hist_kws={'edgecolor':'black'}).set_title('Распределение стажа работы')
sb.distplot(CB['Salary'], hist=True, kde=True, 
             color = 'darkblue', 
             hist_kws={'edgecolor':'black'}).set_title('Распределение заработной платы')

# Правило 3-х сигм для заработной платы
print("Выбросы заработной платы по правилу трёх сигм: ")
for x in CB['Salary']:
    if (abs(x - np.mean(CB['Salary']) >  
    3 * np.std(CB['Salary']))):
        print(x)



# Анализ качественных переменных

CB['Gender'].value_counts().plot(kind='bar', ylabel='frequency')
plt.xlabel("Пол")
plt.show()

CB['Seniority_level'].value_counts().plot(kind='bar', ylabel='frequency')
plt.xlabel("Грейд")
plt.show()

# Так как очень много городов, оставляем только те, которые чаще всего встречаются
dic = Counter(CB['City'])
most_common = dic.most_common(15)
most_common_array = []
for item in most_common:
    most_common_array = np.append(most_common_array, item[0])
newlist = []
for i in range(0, np.size(CB['City'])):
    if (CB['City'][i] in most_common_array):
        newlist = np.append(newlist, CB['City'][i])
    else:
        newlist = np.append(newlist, 'Другие')
plt.hist(newlist, edgecolor='black')
plt.xlabel("Город")
plt.xticks(rotation = 70)
plt.show()

# Так как очень много вариантов должностей, оставляем только те, которые чаще всего встречаются
dic = Counter(CB['Position'])
most_common = dic.most_common(15)
most_common_array = []
for item in most_common:
    most_common_array = np.append(most_common_array, item[0])
newlist = []
for i in range(0, np.size(CB['Position'])):
    if (CB['Position'][i] in most_common_array):
        newlist = np.append(newlist, CB['Position'][i])
    else:
        newlist = np.append(newlist, 'Другие')
plt.hist(newlist)
plt.xlabel("Должность")
plt.xticks(rotation = 70)
plt.show()


#Анализ статистической связи.

# Скорее всего нужно убрать выброс (одну з.п в 500000000), тогда график норм будет
sb.boxplot(data=CB, x="Age", y="Salary")
