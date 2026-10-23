import requests


def check_metric_annotation_safety(payload):
    response = requests.post('https://api.example.com/v1/check-annotation-safety', json=payload)
    response.raise_for_status()
    return response.json()