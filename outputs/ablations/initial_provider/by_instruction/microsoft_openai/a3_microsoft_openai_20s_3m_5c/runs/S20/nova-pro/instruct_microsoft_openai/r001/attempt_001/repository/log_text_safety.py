import os
import json
import requests

from observability_client import ObservabilityClient

def check_log_text_safety(log_text):
    client = ObservabilityClient()
    safety_check = client.check_safety(log_text)
    return safety_check

if __name__ == '__main__':
    log_text = 'User logged in successfully'
    result = check_log_text_safety(log_text)
    print(result)