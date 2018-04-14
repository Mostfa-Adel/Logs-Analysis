# news database report project:
it prints a report about news postgresql database that holds data for a part of news website 

that has 3 tables
log, articles, authors

it answer some common questions for database:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## required installation 
postgre sql and python 3 on your virtual machine

(you might need to install psycopg DB-API library)

## run project
1. download newsdata.zip file: 
[here]
(https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) 
2. extract newsdata.sql file and put it beside news.py file
3. create views that will be in next section
4. run `news.py` python file

## views creation
### frirst view:
```sql 
CREATE view days_errors AS

SELECT DATE(time) AS d, COUNT(*) AS c FROM log

WHERE status='404 NOT FOUND'

GROUP BY d;
```

### second view:
```sql 
CREATE VIEW days_requests AS

SELECT DATE(time) AS d, COUNT(*) AS c FROM log

GROUP BY d;
```

## more details on news.py
### functions: 

#### `print_results()`:

take a title and a list and displays them in a good format

#### `display_query_result()`:

take query and title and gets query results from news database and display them
then close connection that it had opened

#### `db_connect(dbname)`:

take db name and try connecting to it and reurn connection and cursor

#### `display_articles()`, `display_authors()`, `display_days_errors()` :

displays the query results for our three questions using  `display_query_results()`
after preparing right query.