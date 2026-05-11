from sqlalchemy import text, create_engine

def query_commit(query, con):
    conn.execute(text(query))
    conn.commit()

host = "dpg-d7prd0l7vvec73fh8l00-a.oregon-postgres.render.com"
user = "admin123"
pswd = "Zfqw6iRCvkK538qgEUGMddFDCro6Exp6"
database = "dw_g739"
string_conn = f"postgresql+psycopg2://{user}:{pswd}@{host}/{database}"

engine = create_engine(string_conn)
conn = engine.connect()

# Schemas
print("Criando Schemas")
query_commit("create schema if not exists staging", conn)
query_commit("create schema if not exists datamart", conn)

# Data Mart Tables

tables = {
    "datamart.D_FORMATO": """
CREATE TABLE IF NOT EXISTS datamart.D_FORMATO AS
SELECT 
    format_id,
    format_desc
FROM staging.format
    """,

    "datamart.D_PUBLICADOR": """
CREATE TABLE IF NOT EXISTS datamart.D_PUBLICADOR AS
SELECT DISTINCT
    pub_id,
    name,
    city,
    state,
    country,
    year_established,
    marketing_spend
FROM staging.publisher
WHERE name != 'Cedar House Publishers'
    """,

    "datamart.D_LIVRO": """
CREATE TABLE IF NOT EXISTS datamart.D_LIVRO as
SELECT 
    i.book_id,
    i.volume_number,
    b.title,
    s."Unnamed: 0" AS series_name,
    g.genre_desc AS genre,
    a.first_name AS author_first_name,
    a.last_name AS author_last_name,
    to_timestamp(a.birthday, 'DD/MM/YYYY') AS author_birth_day,
    a.country_residence AS author_country_residence,
    a.hrs_writing_day AS author_hours_writting_day
FROM staging.info i
LEFT JOIN staging.book b ON b.book_id = i.book_id 
LEFT JOIN staging.author a ON a.author_id = b.author_id
LEFT JOIN staging.series s ON s.series_id = i.series_id 
LEFT JOIN staging.genders g ON g.genre_id = i.genre_id
    """,

    "datamart.F_VENDA": """
CREATE TABLE IF NOT EXISTS datamart.F_VENDA as
SELECT 
    e.book_id,
    e.format_id,
    e.pub_id,
    e.isbn,
    cast(e.pages as int) as pages,
    cast(e.price as float) as price,
    cast(s.discount as float) as discount,
    to_timestamp(s."Unnamed: 0", 'DD/MM/YYYY') as sale_date,
    to_timestamp(e.publication_date, 'DD/MM/YYYY') as publication_date
FROM staging.sales s
LEFT JOIN staging.edition e ON s.isbn = e.isbn 
WHERE s.isbn IS NOT NULL
    """,

}

for name, query in tables.items():
    print(f"Criando Tabela: {name}")
    query_commit(f"drop table if exists {name}", conn)
    query_commit(query, conn)
