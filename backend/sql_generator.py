from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_sql(question):

    prompt = f"""
You are a PostgreSQL expert.

Database Schema:

customers(
    customer_id,
    customer_name,
    email,
    city,
    country,
    signup_date
)

products(
    product_id,
    product_name,
    category,
    price,
    stock
)

orders(
    order_id,
    customer_id,
    order_date,
    total_amount
)

order_items(
    item_id,
    order_id,
    product_id,
    quantity,
    subtotal
)

Rules:
1. Generate ONLY PostgreSQL SELECT queries.
2. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE.
3. Return ONLY SQL.
4. Do not use markdown code blocks.

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    sql = response.text.strip()

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    return sql.strip()