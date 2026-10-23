import requests


def translate_dashboard_note(payload):
    response = requests.post('https://api.example.com/v1/translate-dashboard-note', json=payload)
    response.raise_for_status()
    return response.json()