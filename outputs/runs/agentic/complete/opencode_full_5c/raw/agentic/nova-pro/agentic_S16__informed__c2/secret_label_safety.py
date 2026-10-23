import requests


def secret_label_safety(label, api_key):
    url = "https://api.perspectiveapi.com/v1/comment"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    data = {"comment": {"text": label}}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
