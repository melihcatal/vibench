import os
import json
import requests

from observability_client import ObservabilityClient

def incident_summary(logs):
    client = ObservabilityClient()
    summary = client.summarize_logs(logs)
    return summary

if __name__ == '__main__':
    logs = [
        {
            'timestamp': '2026-09-21T12:34:56Z',
            'level': 'ERROR',
            'message': 'User login failed',
            'userId': '12345'
        },
        {
            'timestamp': '2026-09-21T12:35:00Z',
            'level': 'ERROR',
            'message': 'User session expired',
            'userId': '12345'
        }
    ]
    result = incident_summary(logs)
    print(result)