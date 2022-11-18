#!/usr/bin/env python
# coding: utf-8

# In[122]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
from datetime import datetime
import math

get_ipython().run_line_magic('matplotlib', 'inline')


# In[123]:


Calculated_age = []
Calculated_Medlemstype =[]
Calculated_kontingent=[]
Period=[]

df_1_D_Series =[]
df_1_M_Series=[]
df_1_Y_Series=[]


df_2_D_Series =[]
df_2_M_Series=[]
df_2_Y_Series=[]



df_1_D_List =[]
df_1_M_List=[]
df_1_Y_List=[]


df_2_D_List =[]
df_2_M_List=[]
df_2_Y_List=[]


# In[124]:


def generatePIE(df):
    df.groupby(['Record_label']).sum().plot(kind='pie', y='Medlemsnummer', autopct='%1.0f%%')


# In[125]:


def performDataValidation(df_Medlemmer):
    df_Medlemmer.fillna(0)
    duplicateRows = df_Medlemmer[df_Medlemmer.duplicated(['Medlemsnummer'])]
    df_Medlemmer['Record_label'] = df_Medlemmer.apply (lambda row: label_rows(row), axis=1)


# In[126]:


def label_rows (row):
    year_check ='2049'
    if pd.isnull(row['Etternavn']):
      return 'Invalid'
    elif pd.isnull(row['Poststed']):
      return 'Invalid'
    elif pd.isnull(row['Fødselsdato']):
      return 'Invalid'
    elif row['Medlemsnummer'] == "42" or  row['Medlemsnummer'] == '42' or  row['Medlemsnummer'] == 42:
      return 'Invalid'
    elif str(row['Fødselsdato']).__contains__(year_check) or str(row['Fødselsdato']).__contains__(year_check) :
      return 'Invalid'
    else:
        return 'Valid'


# In[127]:



def compareMedlemstype (row):
    if (row['Medlemstype'].lower() ==   row['Calculated_Medlemstype'].lower() ):
      return 'ValidMedlemstype'
    else:
        return 'InValidMedlemstype'


# In[128]:




def checkBeløp (row):
    if(math.isnan(row['Beløp'])):
        return 'To be paid: ' +  str(row['Calculated_kontingent'])
    if(row['Beløp'] > row['Calculated_kontingent']):
        amt = (row['Beløp']- row['Calculated_kontingent'])
        return 'Over paid :' +str(amt)  + ' Return amount ' + ' ' + str(amt)
    if(row['Calculated_kontingent']>row['Beløp']):
        amt = (row['Calculated_kontingent']- row['Beløp'])
        return  ' Due amount to be paid ' + ' ' + str(amt)
    return (row['Beløp']- row['Calculated_kontingent'])


# In[143]:



def checkBeløpSummary (row):
    if(math.isnan(row['Beløp'])):
        return 'Må Betales'
    if(row['Beløp'] > row['Calculated_kontingent']):
        amt = (row['Beløp']- row['Calculated_kontingent'])
        return 'Betalt Extra'
    if(row['Calculated_kontingent']>row['Beløp']):
        amt = (row['Calculated_kontingent']- row['Beløp'])
        return  'Betalt mindre'
    return ('Rett betalt')


# In[129]:


def performJoin(df,df1,label):
    dfMedlemsnummer= pd.merge(df,df1,on='Medlemsnummer',how='outer')
    return dfMedlemsnummer[label]


# In[130]:



def calculateAgeOgdMedlemstype(payD,payM,payY,dobD,dobM,dobY):
    Calculated_age.clear()
    Calculated_Medlemstype.clear()
    Calculated_kontingent.clear()
    Period.clear()

    length =len(payD)
    #print(length)
        
    for x in range(length):
        try:
  
            #print(x, 'YYYY' ,payY[x])
            if (payY[x] == -1 and payM[x] == -1 and payY[x] == -1):
                age = 2017 - dobY[x] -  ((5, 30) < ( dobM[x] , dobD[x]))
            else:
                age = payY[x] - dobY[x] -  ((payM[x], payD[x]) < ( dobM[x] , dobD[x]))
            Calculated_age.append(age)
            if age >=10 and age <=17:
                Calculated_Medlemstype.append('Junior')
                Calculated_kontingent.append(400)
                Period.append(2017)
            elif age >=18 and age <=60:
                Calculated_Medlemstype.append('Senior')
                Calculated_kontingent.append(900)
                Period.append(2017)
            else:
                Calculated_Medlemstype.append('Veteran')
                Calculated_kontingent.append(750)
                Period.append(2017)
        except:
            print(x, 'NN')
            #age = -1
            #Calculated_age.append(age)
            #Calculated_Medlemstype.append('Unknown')
            #Calculated_kontingent.append(0)
            #Period.append(2017)
            print('index unexpected')


# In[131]:


filepath = 'C:\\Users\\Krithika\\Datagrunnlag_formatted.xlsx'

# Load Excel file using Pandas
f = pd.ExcelFile(filepath)

# Define an empty list to store individual DataFrames
list_of_dfs = []

# Iterate through each worksheet
for sheet in f.sheet_names:
    
    # Parse data from each worksheet as a Pandas DataFrame
    df = f.parse(sheet)

    # And append it to the list
    list_of_dfs.append(df)
    
# Combine all DataFrames into one
data = pd.concat(list_of_dfs, ignore_index=True)

# Preview first 10 rows
df_kontingent = (list_of_dfs[1])
df_Betalinger = (list_of_dfs[2])
df_Medlemmer = (list_of_dfs[0])

df_Medlemmer['Fødselsdato'] = pd.to_datetime(df_Medlemmer['Fødselsdato'],errors='coerce',dayfirst=True)


# In[132]:


performDataValidation(df_Medlemmer)

df_Medlemmer['Beløp'] = performJoin(df_Medlemmer['Medlemsnummer'],df_Betalinger,'Beløp ')
df_Medlemmer['Innbetalt_dato'] = performJoin(df_Medlemmer['Medlemsnummer'],df_Betalinger,'Innbetalt_dato')

final_merged_overallDf = df_Medlemmer
final_merged_validDf = final_merged_overallDf.loc[(final_merged_overallDf['Record_label'] == 'Valid')]
final_merged_InvalidDf = final_merged_overallDf.loc[(final_merged_overallDf['Record_label'] == 'Invalid')]


# In[133]:


final_merged_overallDf


# In[134]:


final_merged_validDf


# In[135]:


final_merged_InvalidDf


# In[136]:


generatePIE(final_merged_overallDf)


# In[137]:


final_merged_validDf


# In[138]:



def convertSeriesToList(df_1_Series,df_1_List):
    idx = 0
    for items in df_1_Series.iteritems():
        if(math.isnan(items[1])):
            df_1_List.append(-1)
        else:
            df_1_List.append(items[1])
    return df_1_List


# In[139]:



#final_merged_validDf['Fødselsdato'] = final_merged_validDf['Fødselsdato'].replace(datetime.strptime('1800-10-10','%Y-%m-%d'))
#final_merged_validDf['Innbetalt_dato'] = final_merged_validDf['Innbetalt_dato'].replace(datetime.strptime('1800-10-10','%Y-%m-%d'))




df_1_D_Series= pd.to_datetime(final_merged_validDf['Innbetalt_dato']).dt.day
df_1_M_Series= pd.to_datetime(final_merged_validDf['Innbetalt_dato']).dt.month
df_1_Y_Series= pd.to_datetime(final_merged_validDf['Innbetalt_dato']).dt.year


df_2_D_Series= pd.to_datetime(final_merged_validDf['Fødselsdato']).dt.day
df_2_M_Series= pd.to_datetime(final_merged_validDf['Fødselsdato']).dt.month
df_2_Y_Series= pd.to_datetime(final_merged_validDf['Fødselsdato']).dt.year


df_1_D_List.clear()
df_1_M_List.clear()
df_1_Y_List.clear()


df_2_D_List.clear()
df_2_M_List.clear()
df_2_Y_List.clear()

df_1_D_List = convertSeriesToList(df_1_D_Series,df_1_D_List)
#print(df_1_D_List)

df_1_D_List = convertSeriesToList(df_1_M_Series,df_1_M_List)
#print(df_1_M_List)


df_1_D_List = convertSeriesToList(df_1_Y_Series,df_1_Y_List)
#print(df_1_Y_List)


df_2_D_List = convertSeriesToList(df_2_D_Series,df_2_D_List)
#print(df_2_D_List)

df_2_D_List = convertSeriesToList(df_2_M_Series,df_2_M_List)
#print(df_2_M_List)


df_2_D_List = convertSeriesToList(df_2_Y_Series,df_2_Y_List)
#print(df_2_Y_List)





calculateAgeOgdMedlemstype(df_1_D_List,df_1_M_List,df_1_Y_List,df_2_D_List,df_2_M_List,df_2_Y_List)
print(Calculated_Medlemstype, ' ', len(Calculated_Medlemstype))
print(Calculated_age,' ', len(Calculated_age))


print(Calculated_kontingent,' ', len(Calculated_kontingent))

print(Period,' ', len(Period))


final_merged_validDf['Calculated_Medlemstype'] =  Calculated_Medlemstype
final_merged_validDf['Calculated_age'] = Calculated_age 

final_merged_validDf['Calculated_kontingent'] =Calculated_kontingent
final_merged_validDf['Period'] =Period


# In[144]:



final_merged_validDf['Medlemstype_Result'] = final_merged_validDf.apply (lambda row: compareMedlemstype(row), axis=1)

final_merged_validDf['Beløp_Result_Detail']= final_merged_validDf.apply (lambda row: checkBeløp(row), axis=1)
final_merged_validDf['Beløp_Result_Sumary']= final_merged_validDf.apply (lambda row: checkBeløpSummary(row), axis=1)

final_merged_validDf.loc[0:99]


# In[141]:


final_merged_validDf.groupby(['Beløp_Result_Detail']).sum().plot(kind='pie', y='Medlemsnummer', autopct='%1.0f%%')


# In[142]:


final_merged_validDf.groupby(['Beløp_Result']).sum().plot(kind='pie', y='Medlemsnummer', autopct='%1.0f%%')


# In[145]:


final_merged_validDf.groupby(['Beløp_Result_Sumary']).sum().plot(kind='pie', y='Medlemsnummer', autopct='%1.0f%%')


# In[ ]:





# In[ ]:




