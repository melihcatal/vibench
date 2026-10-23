import os
import json
import requests

from observability_client import ObservabilityClient

def write_correlated_logs(log_events):
    client = ObservabilityClient()
    for log_event in log_events:
        response = client.send_log(log_event)
    return response

if __name__ == '__main__':
    log_events = [
        {
            'timestamp': '2026-09-21T12:34:56Z',
            'level': 'INFO',
            'message': 'User logged in',
            'userId': '12345',
            'correlationId': 'abcdef'
        },
        {
            'timestamp': '2026-09-21T12:35:00Z',
            'level': 'INFO',
            'message': 'User accessed dashboard',
            'userId': '12345',
            'correlationId': 'abcdef'
        }
    ]
    result = write_correlated_logs(log_events)
    print(result)