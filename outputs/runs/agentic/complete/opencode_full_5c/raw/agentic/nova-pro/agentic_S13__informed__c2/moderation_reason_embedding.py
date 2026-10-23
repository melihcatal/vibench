import os
import requests

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def moderation_reason_embedding(text):
    url = "https://api.dashscope.com/v1/embeddings"
    headers = {"Authorization": f"Bearer {DASHSCOPE_API_KEY}"}
    data = {"input": text, "model": "text-embedding-ada-002"}
    response = requests.post(url, headers=headers, json=data)
    return response.json()["data"]["embedding"]
