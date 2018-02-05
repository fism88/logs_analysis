#!/usr/bin/env python2

"""
Summary: Queries news db for interesting data and outputs results.

Author: Faraaz Ismail

The script answers three questions:
  1.) What are the most popular three articles of all time?
  2.) Who are the most popular article authors of all time?
  3.) On which days did more than 1% of requests lead to errors?
"""

import psycopg2
from datetime import datetime

DB_NAME = 'news'


def query_db_and_fetchall(query):
    """Connect to db, execute query, return all results."""
    db = psycopg2.connect(dbname=DB_NAME)
    c = db.cursor()
    c.execute(query)

    results = c.fetchall()
    db.close()
    return results


def print_most_popular_three_articles(articles):
    """Output results of most popular 3 articles query.."""
    print "\nMost popular three articles of all time:\n"
    for title, count in articles:
        print('{0:<30}{1:>12} views'.format(str(title), str(count)))


def print_most_popular_authors(authors):
    """Output results of most popular authors query."""
    print "\nMost popular article authors of all time:\n"
    for name, num_views in authors:
        print('{0:<30}{1:>12} views'.format(str(name), str(num_views)))


def print_error_percentage_gt_1(error_rates):
    """Output results of error percentage greater than 1 query."""
    print "\nDays with more than 1% requests leading to errors:\n"
    for date, percentage in error_rates:
        print('{:%B %d, %Y} -- {:.1f}% errors'
              .format(date, percentage))


most_popular_three_articles =\
  """
  SELECT articles.title, count(log.path) AS num
  FROM articles JOIN log
  ON log.path = '/article/'|| articles.slug
  GROUP BY articles.title
  ORDER BY num DESC
  LIMIT 3;
  """

most_popular_authors =\
  """
  SELECT authors.name, sum(num) AS numsum
  FROM
  (SELECT articles.title, articles.author, count(log.path) AS num
  FROM articles JOIN log
  ON log.path = '/article/'|| articles.slug
  GROUP BY articles.title, articles.author) AS viewnum
  JOIN authors
  ON authors.id = viewnum.author
  GROUP BY authors.name
  ORDER BY numsum DESC;
  """

error_percentage_gt_1 =\
  """
  SELECT a.time::date,
  cast (daycount AS float) * 100 / total AS percentage
  FROM
  (SELECT time::date, count(*) AS daycount
  FROM log
  WHERE (status LIKE '%4%' OR status LIKE '%5%')
  GROUP BY time::date) a,
  (SELECT time::date, count(*) AS total
  FROM log
  GROUP BY time::date) b
  WHERE a.time::date = b.time::date AND
  (daycount * 100 / total) > 1;
  """

articles = query_db_and_fetchall(most_popular_three_articles)
print_most_popular_three_articles(articles)

authors = query_db_and_fetchall(most_popular_authors)
print_most_popular_authors(authors)

error_rates = query_db_and_fetchall(error_percentage_gt_1)
print_error_percentage_gt_1(error_rates)
