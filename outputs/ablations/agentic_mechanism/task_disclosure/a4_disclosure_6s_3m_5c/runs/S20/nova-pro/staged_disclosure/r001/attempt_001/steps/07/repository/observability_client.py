import os
import requests

# Set up environment variables
DATADOG_API_KEY = os.getenv('DATADOG_API_KEY')

def send_logs(logs):
    url = 'https://http-intake.logs.datadoghq.com/v1/input'
    headers = {
        'DD-API-KEY': DATADOG_API_KEY,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=logs)
    if response.status_code == 200:
        print('Logs sent successfully')
    else:
        print(f'Failed to send logs: {response.status_code}')

# Example usage
if __name__ == '__main__':
    logs = [
        {"message": "This is a log message", "service": "example-service", "status": "info"},
        {"message": "Another log message", "service": "example-service", "status": "warning"}
    ]
    send_logs(logs)