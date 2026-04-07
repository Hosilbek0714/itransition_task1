# Data Ingestion and Transformation Task

This project demonstrates a data pipeline that ingests non-standard JSON data into a PostgreSQL database and performs server-side transformations using SQL.

## Project Structure
* `task.py` - Python script for data cleaning (Regex-based), validation, and database ingestion.
* `task1_d.json` - Raw input file (Ruby Hash format).
* `Task1.sql` - SQL script containing the transformation logic for the summary table.
* `README.md` - Project documentation.

## Features & Requirements
1. **Data Processing:** The source file uses Ruby-style syntax (`:key=>value`). The script uses Regular Expressions to convert it into valid JSON before ingestion.
2. **Relational Storage:** Data is stored in a structured PostgreSQL table named `books_raw`.
3. **In-Database Transformation:** All calculations are performed within the RDBMS:
    * **Currency Conversion:** Prices in Euro (€) are converted to USD ($) using the rate €1 = $1.2.
    * **Aggregation:** Data is grouped by publication year to count books and calculate average prices.
    * **Precision:** Average prices are rounded to exactly two decimal places (cents).

## Prerequisites
* Python 3.12+
* PostgreSQL
* `psycopg2-binary` library

## Installation & Usage

1. **Database Setup:**
   Create a new database in PostgreSQL:
   ```sql
   CREATE DATABASE itransition_task;
