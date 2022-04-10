import numpy as np
import pandas as pd

import plotly.express as px
import time
import seaborn as sns
import os

filename= 'Data-Table 1.csv'



def readCSV(filename):
    population_df= pd.read_csv(filename,skiprows=1)

    return population_df


def sumAll(x):
 
    other_columns=['1960', '1961', '1962', '1963', '1964',
       '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973',
       '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982',
       '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991',
       '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000',
       '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
       '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018',
       '2019', '2020']
    y=0
    for col in other_columns:
        y+=x[col]   
        #print(y)
    return y

def addTotalPopulation():
    population_df= readCSV(filename)    
    population_df['Total']=  population_df.apply(lambda x: sumAll(x),axis=1)

    return population_df


def byCountryData():
    population_df= readCSV(filename)
    country_name= population_df['Country Name'].to_list()
    population_dft= population_df.drop(['Country Code'], axis =1)
    population_dft= population_dft.transpose()

    df_columns= population_dft.iloc[0]

    population_dft.columns= df_columns
    population_dft= population_dft.drop(population_dft.index[0])

    for country in country_name[10:15]:
        fig= px.line(population_dft, x= f"{country}")
        fig.show()


def plotPieGrapgh():
    totalpopulation= addTotalPopulation()
    #sort total values
    sorted_popultation=totalpopulation.sort_values('Total')

   
    #get area under the graph be equal 
    new_range= np.linspace(0,len(sorted_popultation),15)

    for index, n in enumerate(new_range[:-1]):
    
        start=int(new_range[index])
        end=int(new_range[index+1])
        n_df= sorted_popultation.iloc[start:end]
        fig = px.pie(n_df, values='Total', names='Country Name')
        fig.show()

if __name__ =='__main__':
    start_time= time.time()

    plotPieGrapgh()
    byCountryData()

    print(f'Code finisehd in: {time.time()-start_time}')



