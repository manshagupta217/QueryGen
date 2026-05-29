from fastapi import FastAPI
from pydantic import BaseModel
from database import get_connection
from sql_generator import generate_sql

app = FastAPI(
    title="QueryGen API",
    description="AI-Powered Natural Language to SQL Generator",
    version="1.0"
)

class Question(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Welcome to QueryGen",
        "status": "running"
    }


@app.get("/customers")
def get_customers():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT customer_name,email
        FROM customers
        LIMIT 10
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


@app.post("/query")
def query(data: Question):

    sql = generate_sql(data.question)

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    # Security Check
    forbidden_keywords = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "CREATE",
        "TRUNCATE"
    ]

    if any(keyword in sql.upper() for keyword in forbidden_keywords):
        return {
            "error": "Only SELECT queries are allowed."
        }

    if not sql.upper().startswith("SELECT"):
        return {
            "error": "Generated query is not a SELECT statement."
        }

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute(sql)

        columns = [desc[0] for desc in cur.description]

        rows = cur.fetchall()

        results = []

        for row in rows:
            results.append(
                dict(zip(columns, row))
            )

        return {
            "question": data.question,
            "generated_sql": sql,
            "row_count": len(results),
            "results": results
        }

    except Exception as e:

        return {
            "error": str(e),
            "generated_sql": sql
        }

    finally:
        cur.close()
        conn.close()