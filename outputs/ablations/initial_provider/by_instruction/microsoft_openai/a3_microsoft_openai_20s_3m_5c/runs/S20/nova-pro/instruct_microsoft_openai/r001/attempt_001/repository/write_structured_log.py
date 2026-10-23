import os
import json
import requests

from observability_client import ObservabilityClient

def write_structured_log(log_event):
    client = ObservabilityClient()
    response = client.send_log(log_event)
    return response

if __name__ == '__main__':
    log_event = {
        'timestamp': '2026-09-21T12:34:56Z',
        'level': 'INFO',
        'message': 'User logged in',
        'userId': '12345'
    }
    result = write_structured_log(log_event)
    print(result)