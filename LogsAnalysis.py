#!/usr/bin/env python3
# Logs Analysis Project
# version 1.1.06
# Udacity Nanodegree - Full Stack Development
# Anik Bhattacharya

import datetime
import psycopg2

dbname = "news"

# Connect to the database and return a variable pointing to that connection
def init_db_connection():
    database_connection = psycopg2.connect(database=dbname)
    return database_connection

def run_query(cur, query):
    cur.execute(query)
    result = cur.fetchall()
    return result

# Returns a table showing the top three most-viewed articles
# Columns: article title, number of views for that article
query_1 = """select articles.title, count(*) as views
            from articles join log
            on log.path like concat('%', articles.slug)
            group by articles.title
            order by views desc
            limit 3
            """

# Returns a table showing the most popular authors, sorted in descending order popularity
# Columns: author name, number of total views for all articles by that author
query_2 = """select authors.name, subq.views
            from authors join
                (select articles.author, count(*) as views
                from articles join log
                on log.path like concat('%', articles.slug)
                group by articles.author
                order by views desc
                ) as subq
            on authors.id = subq.author
            """

# Returns a table showing days on which more than 1% of HTTP requests resulted in an error
# Columns: date, percentage of requests that resulted in an error
query_3 = """select req_all.datef, (100.0*req_err.errors/req_all.all_requests) as error_incidence
            from
                (select to_date(to_char(time, 'Month DD, YYYY'), 'Month DD, YYYY') as datef, count(*) as errors
                from log
                where status like '4%'
                group by datef
                ) as req_err
            left join
                (select to_date(to_char(time, 'Month DD, YYYY'), 'Month DD, YYYY') as datef, count(*) as all_requests
                from log
                group by datef
                ) as req_all
            on req_err.datef = req_all.datef
            where (100.0*req_err.errors/req_all.all_requests) > 1.0
            """

# Run queries one by one, format results to be easily readable, and print out results
print("\n#######################################################################")
print("\n##                                                                   ##")
print("\n##     Udacity Full Stack Nanodegree - Logs Analysis Project         ##")
print("\n##     Anik Bhattacharya (anik.bhattacharya.2017@gmail.com)          ##")
print("\n##     Version 1.1.06, completed on 03-10-2018                       ##")
print("\n##                                                                   ##")
print("\n#######################################################################")

# Initialize database connection and set up cursor
dbc = init_db_connection()
c = dbc.cursor()

# Query 1 Printout
print("\n\nAnalytics Question 1: What are the three most popular articles of all time?")
result_1 = run_query(c,query_1)
for item in result_1:
    print("\"" + item[0] + "\" — " + str(item[1]) + " views")

# Query 2 Printout
print("\n\nAnalytics Question 2: Who are the most popular article authors of all time?")
result_2 = run_query(c,query_2)
for item in result_2:
    print("" + item[0] + " — " + str(item[1]) + " views")

# Query 3 Printout
print("\n\nAnalytics Question 3: On which days did more than 1% of requests lead to errors?")
result_3 = run_query(c,query_3)
for item in result_3:
    print("" + item[0].strftime('%B %d, %Y') + " — " + str('%.1f' % item[1]) + "% errors")

# Decorative ending with extra space
print("\n\n#######################################################################\n")

# Kill database connection
dbc.close()
