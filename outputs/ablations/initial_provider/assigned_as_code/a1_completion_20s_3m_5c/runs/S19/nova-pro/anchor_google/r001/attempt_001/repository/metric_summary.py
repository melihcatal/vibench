import requests


def summarize_metric_trends(payload):
    response = requests.post('https://api.example.com/v1/metric-trends', json=payload)
    response.raise_for_status()
    return response.json()