# logs-analysis
Logs Analysis project with Python DB API and PostgreSQL, for Udacity's Full Stack Development Nanodegree

## Table of Contents
- [About](#about)
- [Dependencies](#dep)
- [Installation](#inst)
- [Usage](#use)
  - [Running the Program](#runprog)
  - [Queries and Output](#queries)
    - [Task 1](#task1)
    - [Task 2](#task2)
    - [Task 3](#task3)
- [Output](#output)
<a name="about"></a>
## About
This small repository contains the LogsAnalysis.py python document, which is my submission for the Logs Analysis project in Udacity's Full Stack Web Development Nanodegree. It does not contain the database dependency needed to run the program - please see the [Dependencies](#dep) section for more details.
### Components
- LogsAnalysis.py: Contains the Python code that is executed to run the queries and obtain the results, shown below in the [Usage](#use) section.
- output.txt: Plain text file containing a copy of the full output you should expect to see when the program is executed on a command-line interface.

<a name="dep"></a>  
## Dependencies
The following components are not included in the repository, but are necessary to run this program. These files are provided through Udacity's Full Stack Web Development Nanodegree:
- newsdata.sql: Contains the data that is queried by the LogsAnalysis.py program. This can be downloaded [here, provided you have access](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). Unzip the downloaded zip file to reveal the contents, which should be a single file, `newsdata.sql`.
- You must have a Linux Virtual Machine (VM) available on your computer, with the PostgreSQL database software installed. The data in the *newsdata.sql* file will be stored into a PostgreSQL database on the VM, where these queries will be ultimately run.
- You must have the ***latest version*** of Python 3 installed on your system.
<a name="inst"></a>
## Installation 
#### If you do not have the Linux VM and Python 3 already installed, please refer to the following instructions:
1. First, [visit this site](https://www.virtualbox.org/wiki/Downloads) to download and install the **VirtualBox** VM Environment. *Important*: be sure to install the platform package for your operating system. 
2. Second, [visit this site](https://www.vagrantup.com/downloads.html) to download and install the **Vagrant** configuration program that will install the Linux operating system inside the virtual machine.
3. Lastly, [visit this site](https://www.python.org/downloads/) to install Python 3 on your system. ***Important***: Do not download a version of Python 2. Be sure to download and install ***only the latest version*** of Python 3.
#### To download and install the project files, please follow these instructions:
1. Clone this repository to a local directory.Move the `newsdata.sql` file into the project directory you just cloned.
2. Next, [download this file](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f73b_vagrantfile/vagrantfile), a configuration file called `Vagrantfile`. Place this file inside the root directory for this project, which you had just cloned.
3. In a terminal or command-line interface such as GitBash, change directory with the `cd` command to the project's directory, where the Vagrantfile should now be located. Perform the `ls` command (or its equivalent on your operating system) to verify that it is. 
4. Whenever you're ready, perform the following command to start up the Linux VM: `vagrant up`
5. If this is your first time doing this, vagrant will begin installing the Linux operating system. Once vagrant has finished installing (if first time) and starting up the Linux VM, and installing any updates, you will regain control of the command line interface.
6. Once you've regained control, perform the following command: `vagrant ssh`
7. Now, you will need to change directory, using `cd` to the projects directory. This should be as simple as performing the following command: `cd /logs-analysis`
8. Verify you are in the right directory by printing out its contents with `ls`, or the equivalent for your operating system. You should see the `LogsAnalysis.py` document and the `newsdata.sql` file. If this is the case, you're ready to begin!
<a name="use"></a>
## Usage
### Project Goals
The project analyzes the *news* database (inside dependency *newsdata.sql*) to answer the following analytical questions:
1. What are the three most popular articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of HTTP requests lead to errors?
<a name="runprog"></a>
### Running the Program
If the previous conditions listed in the [Dependencies](#dep) and [Installation](#inst) sections have been met, you're in the right directory, and the aforementioned files can be seen in the directory, you're ready to begin. 

Perform the following command to run the program: 

`python3 LogsAnalysis.py`

If the above command returns an error, you may need to use this command instead: 

`python LogsAnalysis.py`
<a name="queries"></a>
### Queries and Outputs
<a name="task1"></a>
#### Task 1
To solve the first task, the following query was used: 
```
  select articles.title, count(*) as views
  from articles join log
  on log.path like concat('%', articles.slug)
  group by articles.title
  order by views desc
  limit 3
```
The query works by performing an inner join between the *articles* and *log* tables on the condition that, for each row of the log, the precise path of the resource requested/accessed by a visitor contains the particular slug (path extension) pertaining to a specific article. This is accomplished with a "like" statement that searches with a '%' wildcard (since the slug portion is just at the end of the full path). 

The query then groups the results by article title, and displays a table with two columns, article title and total number of views, in descending order of views (starting with the article with the most views), and limits the table to show only the top 3 viewed articles, to yield the following output (after formatting):
```
Analytics Question 1: What are the three most popular articles of all time?
"Candidate is jerk, alleges rival" — 338647 views
"Bears love berries, alleges bear" — 253801 views
"Bad things gone, say good people" — 170098 views
```
<a name="task2"></a>
#### Task 2
To solve the second task, the following query was used: 
```
  select authors.name, subq.views
  from authors join
    (select articles.author, count(*) as views
    from articles join log
    on log.path like concat('%', articles.slug)
    group by articles.author
    order by views desc
    ) as subq
  on authors.id = subq.author
```
This query first performs an inner join with the *articles* and *log* tables, in a manner similar to the one in the first query, matching article slugs with paths in the log. Whereas the query in task 1 organized the resulting table by article title and counted views for each article counted in task 1, this query organizes the resulting table by author id (a unique integer pertaining to each specific author in the *authors* table) and counts the total views for each author (for all articles written by that author).

One more join, this time between the *authors* table and the resultant table from the nested select query, is performed in order to replace the integer id numbers with the names of authors. The final result, after formatting, is:
```
Analytics Question 2: Who are the most popular article authors of all time?
Ursula La Multa — 507594 views
Rudolf von Treppenwitz — 423457 views
Anonymous Contributor — 170098 views
Markoff Chaney — 84557 views
```
<a name="task3"></a>
#### Task 3
To solve the third task, the following query was used:
```
  select req_all.datef, (100.0*req_err.errors/req_all.all_requests) as error_incidence
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
```
This query begins by aggregating two result tables which are themselves created by querying the *log* table. The second of these lists a record for each day there were user visits to the site, and the total number of requests for that particular day. Dates (stored in the original table in 'timestamp with timezone' format) are first converted to a simple year-month-day type format, and results are grouped by day so that the table can show a count of total requests for each day. The first table is created with a similar logic, except that only requests that contain a "4xx" status code (pertaining to an error) are counted (filtered with the "like 4%" statement).

These two tables are then combined with a left join, and the outer query performs an arithmetic calculation, dividing the number of errors by the number of total requests for each day there were user requests to the site, joining the tables on the commonly-shared date column. The records are then filtered by the where statement at the end, so that only days on which errors made up more than 1% of requests are shown. **N.B.** *The reason for the where statement containing the full formula and not simply the column name "error_incidence" is that there was a strange issue occuring in which a "where" statement with the column name would not work (since it is a computed column that does not exist in the original joined table), and neither would a "having" statement, which would return a different, bizarre error. Having the full formula next to a 'where' clause apparently solved the problem.*

The final result of this query, after formatting is:
```
Analytics Question 3: On which days did more than 1% of requests lead to errors?
July 17, 2016 — 2.3% errors
```
<a name="output"></a>
## Output
The *output.txt* file attached inside this repository provides a simple, plain-text copy of the output you can expect to receive when running the LogsAnalysis.py file and executing the queries therein.

