create schema if not exists staging;

create schema if not exists datamart;



CREATE TABLE IF NOT EXISTS datamart.D_FORMATO AS
SELECT 
    format_id,
    format_desc
FROM staging.format

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



SELECT 
	p.name,
	l.title,
	ROUND(SUM(v.price)) as total_price,
	MIN(v.price) as lower_price,
	MAX(v.price) as high_price,
	COUNT(p.name) as quantity_sold,
	MAX(sale_date) - MIN(sale_date) as quantity_days_sold,
	COUNT(DISTINCT CAST(sale_date AS DATE)) as unique_days_sold,
	(SELECT MAX(CAST(sale_date as DATE)) FROM datamart.F_VENDA) - MAX(sale_date) as days_from_last_sold
FROM datamart.F_VENDA v
LEFT JOIN datamart.D_PUBLICADOR p ON p.pub_id    = v.pub_id
LEFT JOIN datamart.D_LIVRO      l ON l.book_id   = v.book_id
LEFT JOIN datamart.D_FORMATO    f ON f.format_id = v.format_id
WHERE l.genre = 'SciFi/Fantasy'
GROUP BY p.name, l.title

-- 2193-12-31
SELECT MAX(CAST(sale_date as DATE))
FROM datamart.F_VENDA

-- ST303
SELECT book_id, title
FROM datamart.D_LIVRO
WHERE title = 'Soft Pliable Truth'

-- SALE_DATE: 2193-12-28
SELECT *
FROM datamart.F_VENDA
WHERE book_id = 'ST303'
ORDER BY sale_date desc
LIMIT 5
