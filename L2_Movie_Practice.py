## Movie Data Processing
## Clean the dataset to enable movie investment analysis
## 14 Sept 2024

# retrieve data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
df_movie = pd.read_csv(r'C:\Users\30A\Downloads\movie_sample_dataset.csv')
df = pd.read_csv('movie_sample_dataset.csv')
print(df.describe())
# print(df.head(10), df.tail(10), df.sample(10))

# ROI per Country
# I : budget
# R : gross

# handle of missing data
# 1. standardise country -> to enable average calculation of gross in country level -> to fill missing gross
# 2. remove rows with missing budget

# print(df[df['gross'].isnull() == True].shape)
# print(df[df['gross'].isnull() == True])
# print(df[df['budget'].isnull() == True])

# average gross
# print(df['gross'].mean())

# df.col_name is interchangeable with df['col_name'], bracket one is better
# print(df[df.director_name == 'Jay Oliva'].head())
# print(df[df.country == 'USA'].head())
# print(df[df.country == 'USA']['gross'].mean())

# 1. find the average gross per country
# print(df.head())
# df['gross'] = np.where(condition, action when true, action when false)
# df['gross'] = np.where(df['gross'].isnull() == True, df['gross'].mean(), df['gross'])
# df['gross'] = np.where(df['gross'].isnull() == True, df[df.country == 'USA']['gross'].mean(), df['gross'])
# print(df['gross'])
# print(df[df['gross'].isnull() == True])

# 2. remove rows from analysis with missing budget
# stick | means Or, & means And
#df2 = df[(df['budget'] > 100)].reset_index(drop=True)
# print(df2.shape)
# print(df2)

# 3. standardise country names
print(df['country'].unique())
df['country'] = np.where(df['country'].isin(['USA', 'usa']), 'United States', df['country'])
df['country'] = np.where(df['country'] == 'UK', 'United Kingdom', df['country'])
print(df['country'].unique())

# df['ROI'] = gross / budget
df['ROI'] = df['gross'] / df['budget']


print(df['ROI'].describe())
# df['ROI'].plot(kind='hist')
# plt.show()

# df3 = df[df['ROI'] < 1000 ].reset_index(drop=True)
# df3['ROI'].plot(kind='hist')

df4 = df[df['ROI'] < 20 ].reset_index(drop=True)
df4['ROI'].plot(kind='hist')
plt.show()

print(df4.groupby('country')['ROI'].describe())

# splitting column
print('Leonardo DiCaprio,Matthew McConaughey,Jon Favreau'.split(','))
# df4['actors'].str.split(',')
# print(df4)

df_actor = df['actors'].str.split(',', expand=True)
print(df_actor.columns)
print(df.columns)

df['Actor_1'] = df_actor[0]
df['Actor_2'] = df_actor[1]
df['Actor_3'] = df_actor[2]

print(df.head())

df_avg_mean = df.groupby('country')['gross'].mean()
# df['gross'].fillna(0,inplace=True)
# df['gross'] = df['gross'].fillna(df['country'].map(df_avg_mean))
# Apply the mean of each country to the missing 'gross' values
df['gross'] = df.apply(lambda row: df_avg_mean[row['country']] if np.isnan(row['gross']) else row['gross'], axis=1)
df =  df[~df['gross'].isnull()]
print(df.groupby('country')['gross'].mean())
