import psycopg2

def get_connection():
    conn= psycopg2.connect(
        dbname="querygen",
        user="mansagupta",
        host="localhost"
    )
    return conn