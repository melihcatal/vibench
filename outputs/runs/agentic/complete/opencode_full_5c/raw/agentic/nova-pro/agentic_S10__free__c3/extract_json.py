import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"


def extract_json(text):
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
