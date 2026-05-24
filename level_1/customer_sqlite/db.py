import os
import sqlite3
import csv
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class QueryDB:
    def __init__(self, db_name='sales.db'):
        self.db_name = db_name
        self.curr = None
    
    def get_cursor(self):
        conn = sqlite3.connect(self.db_name)
        if self.curr: return self.curr
        self.curr = conn.cursor()
        return self.curr

    def execute_query(self, query):
        try:
            self.curr.execute(query)
            rows = self.curr.fetchall()
            return rows
        except Exception as err:
            logger.error("Query failed with %s", err)

    def get_sql_statement(self, sql_file):
        try:
            with open(os.path.join(BASE_DIR, 'queries', sql_file)) as f:
                statement = f.read()
            return statement
        except Exception as err:
            logger.error("Query failed with %s", err)
        return ''
    
    def close_connection(self):
        self.curr.close()
        self.curr = None

def create_tables():
    create_query = """
        CREATE TABLE IF NOT EXISTS  orders(
        id             INTEGER PRIMARY KEY,
        customer_id    INTEGER,
        product        TEXT,
        amount         REAL,
        status         TEXT,
        region         TEXT,
        category       TEXT
    );

    CREATE TABLE IF NOT EXISTS customers(
        id      INTEGER PRIMARY KEY,
        name    TEXT,
        region  TEXT,
        tier    TEXT
    );

    """
    logger.info("Creating Customers and Order tables in Sales.db")
    try:
        
        conn = sqlite3.connect("sales.db") 
        curr = conn.cursor()
        curr.executescript(create_query)

        logger.info("Loading Orders data into Sales.db")
        with open(os.path.join(BASE_DIR, "datasets","data.csv")) as csv_f:
            for row in csv.DictReader(csv_f):
                curr.execute("INSERT INTO orders VALUES (?,?,?,?,?,?,?)",
                (row['id'], row['customer_id'], row['product'],
                row['amount'], row['status'], row['region'], 
                row.get('category', 'uncategorised'))
                )
        
        logger.info("Loading Customers data into Sales.db")
        with open(os.path.join(BASE_DIR, "datasets","customer.csv")) as csv_f:
            for row in csv.DictReader(csv_f):
                curr.execute("INSERT INTO customers VALUES (?,?,?,?)",
                            (row['id'], row['name'],row['region'], row['tier'])
                        )

        conn.commit()
        logger.info("Database created: sales.db with orders and customers.")
    except Exception as err:
        logger.error("Query failed with %s", err)
    finally:
        conn.close()


if __name__ == '__main__':
    create_tables()

