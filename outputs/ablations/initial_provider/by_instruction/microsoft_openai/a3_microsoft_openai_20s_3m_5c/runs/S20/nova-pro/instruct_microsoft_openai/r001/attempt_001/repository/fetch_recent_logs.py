import os
import json
import requests

from observability_client import ObservabilityClient

def fetch_recent_logs(field, value, start_time, end_time):
    client = ObservabilityClient()
    response = client.fetch_logs(field, value, start_time, end_time)
    return response

if __name__ == '__main__':
    field = 'userId'
    value = '12345'
    start_time = '2026-09-20T00:00:00Z'
    end_time = '2026-09-21T23:59:59Z'
    result = fetch_recent_logs(field, value, start_time, end_time)
    print(result)