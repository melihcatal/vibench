import requests


def metric_annotation_safety(text):
    url = "https://api.example.com/content-safety"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json",
    }
    data = {"text": text}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
