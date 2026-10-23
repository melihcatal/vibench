import os
import json
import requests
from query_error_logs import query_logs

def fetch_recent_logs(time_range, field_filter):
    query = f'CustomLog | where TimeGenerated > ago({time_range}) | where {field_filter}'
    result = query_logs(query)
    return result

if __name__ == '__main__':\n    time_range = '1h'
    field_filter = 'level == "INFO"'
    logs = fetch_recent_logs(time_range, field_filter)
    print(json.dumps(logs, indent=2))
