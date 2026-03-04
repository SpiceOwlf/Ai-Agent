import os
from dotenv import load_dotenv
from tavily import TavilyClient
import json
import sqlite3
import json
from datetime import datetime

load_dotenv() 
tavily_api_key = os.getenv("TAVILY_API_KEY")
if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY not found in .env")
tavily_client = TavilyClient(api_key=tavily_api_key)



response = tavily_client.search("Latest News on Iran and Iseral")

# data = json.loads(response)

data_dump = json.dumps(response, indent = 2)


# print(response)
print(data_dump)



conn = sqlite3.connect("tavily.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    answer TEXT,
    response_time REAL,
    request_id TEXT,
    payload_json TEXT,
    created_at TEXT
)
""")

# response is the dict returned by Tavily
cur.execute("""
INSERT INTO searches (query, answer, response_time, request_id, payload_json, created_at)
VALUES (?, ?, ?, ?, ?, ?)
""", (
    response.get("query"),
    response.get("answer"),
    float(response.get("response_time", 0)),
    response.get("request_id"),
    json.dumps(response),
    datetime.utcnow().isoformat()
))

conn.commit()
conn.close()
