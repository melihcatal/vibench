import requests


def secret_label_safety(payload, config=None):
    api_url = "https://api.example.com/v1/safety-check"
    headers = {"Authorization": f"Bearer {config['api_key']}"}
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()