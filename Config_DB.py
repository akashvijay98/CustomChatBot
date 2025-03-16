import psycopg2
import asyncpg
import asyncio
async def connect_db():
    return await asyncpg.connect(
        host="localhost",
        database="query_results",
        user="postgres",
        password="postgres",
    )

async def store_result(query, result):
    conn = await connect_db()
    try:
        async with conn.transaction():
            row_exists = await conn.fetch("SELECT 1 FROM queries WHERE query_text = $1", query)

            if(row_exists):
                print(f"Query '{query}' already exists in the table. Skipping insert.")
            else:
                insert_query = "INSERT INTO queries (query_text, result_text) VALUES ($1, $2)"
                await conn.execute(insert_query, result)
    finally:
        await conn.close()


async def get_results():
    conn = await connect_db()
    try:
        select_query = "SELECT * FROM queries"
        rows = await conn.fetch(select_query)
        return rows
    finally:
        await conn.close()
