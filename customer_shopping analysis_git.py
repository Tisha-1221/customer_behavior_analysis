import pandas as pd
df = pd.read_csv('customer_shopping_behavior.csv')
print(df.head())
print(df.info())
print(df.describe())
print(df.isnull().sum())

#filling the review rating col null values according to their category( i.e cloothing, footwear..etc)
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
print(df.isnull().sum())

#changing the column names to similar format
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
df = df.rename(columns={'purchase_amount_(usd)': 'purchase_amount'})
print(df.columns)

# create a new column age_group(grouping age in three diff categories)
labels = ['Young-Adult', 'Adult', 'Middle-Aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels= labels)
print(df[['age', 'age_group']].head(15))

print(df['frequency_of_purchases'].unique())

#creating a new column for frequency of purchase(in no.of days rather than in text)
frequency_mapping    = {
    'Fortnightly': 14,
    'Weekly' : 7,
    'Annually' : 30,
    'Quarterly' : 90, 
    'Bi-Weekly' : 14,
    'Monthly' : 365,
    'Every 3 Months' : 90
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
print(df[['purchase_frequency_days', 'frequency_of_purchases']].head(10))

# to check weather discount and promo_code column has all values similar if yes than drop one of the col
print(df[['discount_applied', 'promo_code_used']].head(10))
print((df['discount_applied'] == df['promo_code_used']).all()) #chaecking if both col have simalarity
df = df.drop('promo_code_used', axis=1) #dropped the promo_code col as no longer needed
print(df.columns)

df.to_csv('cleaned_customer_data.csv', index=False)

#loding the data to sql server mangement
from sqlalchemy import create_engine

# Replace YOUR_SERVER_NAME with your SQL Server instance name.
engine = create_engine(
    r"mssql+pyodbc://YOUR_SERVER_NAME\SQLEXPRESS/CustomerAnalysis"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)

from sqlalchemy import text

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(result.fetchone())

df.to_sql(
    'customer_data',
    con=engine,
    if_exists='replace',
    index=False
)

print("Data successfully loaded into SQL Server!")