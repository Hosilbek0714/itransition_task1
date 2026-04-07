import re
import ast
import psycopg2
from psycopg2 import extras

def main():
    try:
        with open('task1_d.json', 'r', encoding='utf-8') as f:
            content = f.read()

        content = re.sub(r':(\w+)\s*=>', r'"\1":', content)
        data = ast.literal_eval(content)
        print("Fayl muvaffaqiyatli o'qildi.")
    except Exception as e:
        print(f"Fayl o'qishda xato: {e}")
        return

    conn_params = {
        "host": "localhost",
        "database": "itransition_task",
        "user": "postgres",
        "password": "1212",
        "port": 5432
    }

    try:
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        cur.execute("DROP TABLE IF EXISTS books_raw CASCADE;")
        cur.execute("""
            CREATE TABLE books_raw (
                id NUMERIC PRIMARY KEY,
                title TEXT,
                author TEXT,
                genre TEXT,
                publisher TEXT,
                year INTEGER,
                price TEXT
            );
        """)

        insert_query = """
            INSERT INTO books_raw (id, title, author, genre, publisher, year, price)
            VALUES (%(id)s, %(title)s, %(author)s, %(genre)s, %(publisher)s, %(year)s, %(price)s)
        """
        extras.execute_batch(cur, insert_query, data)
        conn.commit()
        print(f"Baza yuklandi: {len(data)} qator.")

        cur.execute("DROP TABLE IF EXISTS book_summary;")
        cur.execute("""
            CREATE TABLE book_summary AS
            SELECT
                year AS publication_year,
                COUNT(*) AS book_count,
                ROUND(AVG(
                    CASE
                        WHEN price LIKE '€%' THEN REPLACE(REPLACE(price, '€', ''), ',', '')::NUMERIC * 1.2
                        WHEN price LIKE '$%' THEN REPLACE(REPLACE(price, '$', ''), ',', '')::NUMERIC
                        ELSE REPLACE(price, ',', '')::NUMERIC
                    END
                )::NUMERIC, 2) AS average_price_usd
            FROM books_raw
            GROUP BY year
            ORDER BY year DESC;
        """)
        conn.commit()
        print("Summary jadvali yaratildi.")

    except Exception as e:
        print(f"Xatolik: {e}")
    finally:
        if 'conn' in locals():
            cur.close()
            conn.close()

if __name__ == "__main__":
    main()