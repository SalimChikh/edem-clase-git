# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 17:08:04 2019
@author: Salim CHIKH
Mean Comparison
MDA EDEM
"""
#Resets ALL (Careful This is a "magic" function then it doesn't run as script) 
#reset -f  

 
# MEDIA DE VENTAS WORKING DAY CON MEDIA DE VENTAS NO WORKING DAYS 



#load basiclibraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

# New libraries
from pandas.api.types import CategoricalDtype #For definition of custom categorical data types (ordinal if necesary)
import scipy.stats as stats  # For statistical inference 
import seaborn as sns  # For hi level, Pandas oriented, graphics

# Get working directory
os.getcwd()

# Change working directory
os.chdir('/Users/salim/Desktop/EDEM/Python/Code')
os.getcwd()

#Reads data from CSV file and stores it in a dataframe called rentals_2011
# Pay atention to the specific format of your CSV data (; , or , .)



wbr = pd.read_csv ("WBR_11_12_denormalized_temp.csv", sep=';', decimal=',')

print(wbr.shape)
print(wbr.head())
print(wbr.info())
#QC OK

# Recode  working day
# To string
wbr["wd_st"] = wbr.workingday
wbr.wd_st = wbr.wd_st.replace(to_replace=0, value="No") #poner No donde hay 0 
wbr.wd_st = wbr.wd_st.replace(to_replace=1, value="Yes")#poner Yes donde hay 1
#To category el orden importa ... NO y despues Si
my_categories=["No", "Yes"]
my_datatype = CategoricalDtype(categories=my_categories, ordered=True)
wbr["wd_cat"] = wbr.wd_st.astype(my_datatype)
wbr.info()

#frequencies
mytable = pd.crosstab(index=wbr["wd_cat"], columns="count") # Crosstab
n=mytable.sum()
mytable2 = (mytable/n)*100
print(mytable2)
plt.bar(mytable2.index, mytable2['count'])
plt.xlabel('Working Day')
plt.title('Figure 5. Percentage of Working Days')

#comparar 2 variables los de dias con Yes y dias con No 
wbr.groupby('wd_cat').cnt.describe()
wbr.groupby('wd_cat').cnt.mean()

#extraer la variable solo las que wd_Cat son yes y la guardo en un objeto cnt_wd
cnt_wd=wbr.loc[wbr.wd_cat=='Yes', "cnt"]

#extraer la variable solo las que wd_Cat son No y la guardo en un objeto cnt_nwd
cnt_nwd=wbr.loc[wbr.wd_cat=='No', "cnt"]

#Hacer un Ttest
stats.ttest_ind(cnt_wd, cnt_nwd, equal_var = False)

#pvalue 0.1105 => el pvalue tiene que ser < 0.05 (95%)

res=stats.ttest_ind(cnt_wd, cnt_nwd, equal_var = False)
print(res)


#CI Meanplot comparacion de media ci -> nivel de confianza (media muestral) los intervalos de confianza no tiene que solapar 
 
ax = sns.pointplot(x="wd_cat", y="cnt" , data =wbr, ci = 95, join=0)



#CI meanplot version2 media general en Verde 
plt.figure(figsize=(5,5))
ax = sns.pointplot(x="wd_cat", y="cnt", data=wbr,ci=95, join=0)
ax.set_ylabel('')

# va de 3000 a 7000 subiendo por 500 
plt.yticks(np.arange(3000, 7000, step=500))

# a partir de donde empieza el grafo 
plt.ylim(2800,6200)

plt.axhline(y=wbr.cnt.mean(),linewidth=1,linestyle= 'dashed',color="green")
props = dict(boxstyle='round', facecolor='white', lw=0.5)
plt.text(0.85, 5400, 'Mean: 4504.3''\n''n: 731' '\n' 't: 1.601' '\n' 'Pval.: 0.110', bbox=props)
plt.xlabel('Working Day')
plt.title('Figure 6. Average rentals by Working Day.''\n')




#EXAMPLE 2 YEARS

wbr.groupby('yr').cnt.mean()
cnt_2011=wbr.loc[wbr.yr ==0, "cnt"]
cnt_2012=wbr.loc[wbr.yr ==1, "cnt"]

res = stats.ttest_ind(cnt_2011, cnt_2012, equal_var = False )
print (res)
print(round(res[0],3),round(res[1],3))




# GRAFIC 

plt.figure(figsize=(5,5))
ax = sns.pointplot(x="yr", y="cnt", data=wbr,capsize=0.05, ci=95, join=0)
ax.set_ylabel('')

# va de 3000 a 7000 subiendo por 500 
plt.yticks(np.arange(3000, 7000, step=500))

# a partir de donde empieza el grafo 
plt.ylim(2800,6200)

plt.axhline(y=wbr.cnt.mean(),linewidth=1,linestyle= 'dashed',color="green")
props = dict(boxstyle='round', facecolor='white', lw=0.5)
plt.text(0.35, 5400, 'Mean: 4504.3''\n''n: 731' '\n' 't: 18.6' '\n' 'Pval.: 0.000', bbox=props)
plt.xticks((0,1), ("2011","2012"))
plt.xlabel('Year')
plt.title('Figure 7. Average rentals by Working Years.''\n')
#plt.savefig('mean_plot_cnt_year_scale2.eps')



# EXAMPLE3 


ax = sns.pointplot(x="weekday", y="cnt", data=wbr,ci=95, join=0)


ax = sns.pointplot(x="season", y="cnt", data=wbr,ci=95, join=0)


ax = sns.pointplot(x="mnth", y="cnt", data=wbr,ci=95, join=0)



ax = sns.pointplot(x="weathersit", y="cnt", data=wbr,capsize=0.05,ci=95, join=1)
plt.axhline(y=wbr.cnt.mean(),linewidth=1,linestyle= 'dashed', color ='green')
plt.xticks((0,1,2), ("Sunny","Cloudy","Rainy"))


