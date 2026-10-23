import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"


def answer_with_context(question, context):
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    payload = {"inputs": context + " " + question}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()
