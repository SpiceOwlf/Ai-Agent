"""
in terminal

sqlite3 tavily.db
.tables
SELECT * FROM searches LIMIT 5;
.quit

OR

sqlite3 -header -column tavily.db "SELECT id, query, request_id, created_at FROM searches ORDER BY id DESC LIMIT 10;"

"""


import os
import sqlite3
from email.message import EmailMessage
import smtplib
from dotenv import load_dotenv

load_dotenv()
DB_PATH = "tavily.db"

# conn = sqlite3.connect("tavily.db")
# cur = conn.cursor()
# cur.execute("SELECT * FROM searches LIMIT 1")
# # cur.execute("SELECT id, query, answer, request_id, created_at FROM searches ORDER BY id DESC LIMIT 5")
# rows = cur.fetchall()

# for r in rows:
#     print(r)

# conn.close()






def fetch_latest_rows(limit=5):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT id, query, answer, response_time, request_id, created_at
        FROM searches
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

def build_email_body(rows):
    if not rows:
        return "No data found in searches table."

    lines = []
    for r in rows:
        lines.append(
            f"""ID: {r['id']}
                Query: {r['query']}
                Answer: {r['answer']}
                Response Time: {r['response_time']}
                Request ID: {r['request_id']}
                Created At: {r['created_at']}
                {'-'*40}"""
            )
    return "\n".join(lines)

def send_email(subject, body):
    user = os.getenv("GMAIL_USER")
    app_password = os.getenv("GMAIL_APP_PASSWORD")
    to_email = os.getenv("EMAIL_TO")

    if not all([user, app_password, to_email]):
        raise ValueError("Missing GMAIL_USER / GMAIL_APP_PASSWORD / EMAIL_TO in .env")

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(user, app_password)
        smtp.send_message(msg)

if __name__ == "__main__":
    rows = fetch_latest_rows(limit=5)
    body = build_email_body(rows)
    send_email("Latest Tavily DB Records", body)
    print("Email sent.")
