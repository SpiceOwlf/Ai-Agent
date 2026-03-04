## 1. what I want to build
A newsletter? tell me the news from yesterday. 
query the internet for 5 most important ones
Store in DB
get the data from DB and let LLM analysis it to me, and feed me as the summary




# To install: pip install tavily-python
from tavily import TavilyClient
client = TavilyClient("tvly-dev-*************************************************")
response = client.search(
    query="",
    search_depth="advanced"
)
print(response)

https://app.tavily.com/certification


## 1.Cloud scheduled job (recommended for reliability)
No full server needed.
Good choices: GitHub Actions (cron), AWS Lambda + EventBridge, Google Cloud Run Job + Scheduler.
Runs even when your laptop is off.