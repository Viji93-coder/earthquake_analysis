import pandas as pd

from urllib.parse import quote_plus

from sqlalchemy import create_engine

password = quote_plus("**********")
engine = create_engine(f'mysql+pymysql://root:{password}@localhost:3306/global')


df = pd.read_csv(
    "data/processed/global_table.csv"
)

df.to_sql(
    "global_table",
    engine,
    if_exists="replace",
    index=False,
    chunksize=1000,
    method="multi"
)

print("Data Loaded Successfully")