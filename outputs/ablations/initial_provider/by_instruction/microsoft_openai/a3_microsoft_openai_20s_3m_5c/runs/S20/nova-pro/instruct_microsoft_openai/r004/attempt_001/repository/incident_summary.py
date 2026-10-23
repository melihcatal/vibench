import os
import json
import requests
from query_error_logs import query_logs

def summarize_error_logs():
    query = 'CustomLog | where severity == "ERROR" | summarize count() by message'
    result = query_logs(query)
    return result

if __name__ == '__main__':\n    summary = summarize_error_logs()
    print(json.dumps(summary, indent=2))
