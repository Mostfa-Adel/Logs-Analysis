#!/usr/bin/env python3.6
import psycopg2
import sys


def print_results(title, result_list):
    """ printing title and data that returned from database
        args: 1-title(string):header of data
              2-result_list(list):list of data to print in some format
    """
    print(title + ':\n')
    for row in result_list:
        r = ''
        for i in range(len(row)):
            r += str(row[i]) + ' -- '
        r = r[:-4]
        print(r)
    print('\n')


def display_query_results(title, q):
    """prints formatted results from news database by query
       args: 1-title(string):header of query results
             2-q(string):sql query for required data
    """
    connect, cursor = db_connect('news')
    cursor.execute(q)
    print_results(title, cursor.fetchall())
    connect.close()


def db_connect(db_name):
    """connects to database and returns connection and cursor
       args: 1-db_name(string):database name to connect
    """
    try:
        connect = psycopg2.connect('dbname=' + db_name)
        cursor = connect.cursor()
        return connect, cursor
    except psycopg2.Error as e:
        print('database connection failed: ' + str(e))
        sys.exit(1)


def display_articles():
    """get the most popular three articles in news database and prints this data"""
    q = """SELECT a.title ,CAST(COUNT(*) AS VARCHAR) || ' visited' AS visited
    FROM articles AS a JOIN log AS l
    ON (l.path = '/article/' || a.slug AND status!='404 NOT FOUND')
    GROUP BY a.title
    ORDER BY COUNT(*) DESC
    LIMIT 3"""
    display_query_results('The most popular articles', q)


def display_authors():
    """prints the most popular authors"""
    q = """
    SELECT au.name, CAST(COUNT(*) AS VARCHAR) || ' visited' AS visited
    FROM articles AS a
    JOIN log AS l
    ON (l.path = '/article/' || a.slug AND status!='404 NOT FOUND')
    JOIN authors AS au
    ON au.id=a.author
    GROUP BY au.name
    ORDER BY COUNT(*) DESC"""
    display_query_results('most popular authors', q)


def display_days_errors():
    """prints the days that has more than 1% errors of request"""
    q = """
    SELECT to_char(r.d,'FMMONTH DD, YYYY'),
    CAST(CAST(100.0 * e.c / r.c AS DEC(4,2)) AS VARCHAR) || ' % Errors'
    FROM days_requests AS r
    JOIN days_errors AS e
    ON e.d=r.d
    WHERE 100.0*e.c/r.c > 1.0
    ORDER BY (100.0 * e.c / r.c ) DESC
    """
    display_query_results('the days that have more than 1% errors', q)


if __name__ == '__main__':
    # these functions connect to db news and get
    # result foreach query then display this data
    display_articles()
    display_authors()
    display_days_errors()
