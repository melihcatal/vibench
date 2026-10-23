import os
import json
import requests

class ObservabilityClient:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.api_url = 'https://api.openai.com/v1/logs'

    def send_log(self, log_event):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post(self.api_url, headers=headers, json=log_event)
        return response.json()

    def query_logs(self, severity, start_time, end_time):
        params = {
            'severity': severity,
            'start_time': start_time,
            'end_time': end_time
        }
        response = requests.get(self.api_url, params=params)
        return response.json()

    def fetch_logs(self, field, value, start_time, end_time):
        params = {
            'field': field,
            'value': value,
            'start_time': start_time,
            'end_time': end_time
        }
        response = requests.get(self.api_url, params=params)
        return response.json()