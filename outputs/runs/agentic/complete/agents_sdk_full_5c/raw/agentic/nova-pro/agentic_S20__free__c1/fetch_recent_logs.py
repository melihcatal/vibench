from datetime import datetime, timedelta
from observability_client import get_logs_query_client

def fetch_recent_logs():
    client = get_logs_query_client()
    query = 'AppTraces
    | where timestamp > ago(1d)
    | where customDimension_MyField == "MyValue"'
    response = client.query('MyWorkspace', query)
    return response.tables[0].rows

recent_logs = fetch_recent_logs()
for log in recent_logs:
    print(log)