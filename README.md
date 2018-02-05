# Logs Analysis Project

## Project Description
The logs_analysis.py script uses pyscopg2 to query a PostgreSQL database for a fictional news website.

The script answers three questions:
  1.) What are the most popular three articles of all time?
  2.) Who are the most popular article authors of all time?
  3.) On which days did more than 1% of requests lead to errors?

The database is structured with three tables:
* articles - includes the articles themselves.
  * author (integer)
  * title (text)
  * slug (text)
  * lead (text)
  * body (text)
  * time (timestamp with time zone)
  * id (integer)
* authors - includes information about the authors of articles.
  * name (text)
  * bio (text)
  * id (integer)
* log - includes one entry for each time a user has accessed the site.
  * path (text)
  * ip (inet)
  * method (text)
  * status (text)
  * time (timestamp with time zone)
  * id (integer)

## Requirements
* Python 2.7
* PostgreSQL
* psycopg2

## Set-Up
* Run `psql -d news -f newsdata.sql` to connect to your installed PostgreSQL database server and execute the SQL commands to set up the schema and load up sample data.
* Run the script with `./logs_analysis.py`.
