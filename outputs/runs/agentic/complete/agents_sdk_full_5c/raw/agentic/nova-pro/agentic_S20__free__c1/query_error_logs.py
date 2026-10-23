from datetime import datetime, timedelta
from observability_client import get_logs_query_client

def query_error_logs():
    client = get_logs_query_client()
    query = 'AppTraces
    | where SeverityLevel == 3
    | where timestamp > ago(1d)'
    response = client.query('MyWorkspace', query)
    return response.tables[0].rows

error_logs = query_error_logs()
for log in error_logs:
    print(log)