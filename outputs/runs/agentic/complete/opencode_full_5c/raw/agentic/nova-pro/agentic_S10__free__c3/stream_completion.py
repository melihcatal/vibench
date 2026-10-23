import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"


def stream_completion(text):
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    payload = {"inputs": text, "stream": True}
    response = requests.post(API_URL, headers=headers, json=payload, stream=True)
    for line in response.iter_lines():
        if line:
            yield line.decode("utf-8")
