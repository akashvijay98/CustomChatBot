import psycopg2
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="query_results",
        user="postgres",
        password="postgres",
    )

def store_result(query, result):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM queries WHERE query_text = %s", (query,))
    if cursor.fetchone():
        print(f"Query '{query}' already exists in the table. Skipping insert.")
    else:
        insert_query = "INSERT INTO queries (query_text, result_text) VALUES (%s, %s)"
        cursor.execute(insert_query, (query, result))
        conn.commit()
    cursor.close()
    conn.close()


def get_results():
    conn = connect_db()
    cursor = conn.cursor()
    select_query = "SELECT * FROM queries"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows