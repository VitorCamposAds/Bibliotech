import pandas as pd
from sqlalchemy import create_engine

host = "dpg-d7prd0l7vvec73fh8l00-a.oregon-postgres.render.com"
user = "admin123"
pswd = "Zfqw6iRCvkK538qgEUGMddFDCro6Exp6"
database = "dw_g739"
string_conn = f"postgresql+psycopg2://{user}:{pswd}@{host}/{database}"

engine = create_engine(string_conn)

tables = [
    "format",
    "publisher",
    "info",
    "book",
    "author",
    "series",
    "genders",
    "sales",
    "edition"
]

for table in tables:
    print(f"Extraindo: {table}")
    url = f"https://raw.githubusercontent.com/xGabrielR/Dataset-Hackday-9/refs/heads/main/{table}.csv"
    df = pd.read_csv(url)

    # Convert to String
    df = df.astype("string")

    df.to_sql(table, schema="staging", index=False, if_exists="replace", con=engine)