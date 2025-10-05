
from mcp.server.fastmcp import FastMCP
import psycopg2
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into environment
serper_api_key = os.getenv("SERPER_API_KEY")
db_conn_string = os.getenv("DB_CONNECTION_STR")


# Create an MCP server
mcp = FastMCP("Medimate")

def init_db():
    conn = psycopg2.connect(db_conn_string)
    return conn, conn.cursor()


@mcp.tool()
def read_psql_db(query: str = "SELECT * FROM patient_record limit 5") -> list:
    """
    Read the patient record from the database
    """
    conn, cursor = init_db()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"Error reading data: {e}")
        return []
    finally:
        conn.close()
        
@mcp.tool()
def google_search(query:str) -> dict:
    """
    Useful for searching the web
    """

    url = "https://google.serper.dev/search"

    payload = json.dumps({
    "q": query, "num":3
    })
    headers = {
    'X-API-KEY': serper_api_key,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()
        

@mcp.tool()
def generate_summary(input:str)-> str:
    """
    Combines all steps to create a user-readable summary.
    Input could be a JSON or compiled string from other tools.
    """
    return input


def main():
    mcp.run(transport='sse')


if __name__ == "__main__":
    main()
