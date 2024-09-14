## Movie Data Processing
## Clean the dataset to enable movie investment analysis
## 14 Sept 2024

# retrieve data
import pandas as pd
import numpy as np

# pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
df_movie = pd.read_csv(r"C:\Users\30A\Downloads\movie_sample_dataset.csv")
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
df['gross'] = np.where(df['gross'].isnull() == True, df[df.country == 'USA']['gross'].mean(), df['gross'])
print(df[df['gross'].isnull() == True])

# remove rows from analysis with missing budget
# stick | means Or, & means And
df2 = df[(df['budget'] > 100)]
print(df2.shape)