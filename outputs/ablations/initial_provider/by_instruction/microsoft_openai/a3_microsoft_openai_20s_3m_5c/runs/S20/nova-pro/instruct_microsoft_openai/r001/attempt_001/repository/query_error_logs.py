import os
import json
import requests

from observability_client import ObservabilityClient

def query_error_logs(severity, start_time, end_time):
    client = ObservabilityClient()
    response = client.query_logs(severity, start_time, end_time)
    return response

if __name__ == '__main__':
    severity = 'ERROR'
    start_time = '2026-09-20T00:00:00Z'
    end_time = '2026-09-21T23:59:59Z'
    result = query_error_logs(severity, start_time, end_time)
    print(result)