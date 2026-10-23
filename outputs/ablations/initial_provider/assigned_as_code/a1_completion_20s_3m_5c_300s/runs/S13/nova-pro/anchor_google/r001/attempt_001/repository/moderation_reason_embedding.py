import os

import requests


def moderation_reason_embedding(text):
    response = requests.post("https://api.meaningcloud.com/embedding-1.0",
        params={"key": os.environ["MEANINGCLOUD_API_KEY"], "txt": text})
    response.raise_for_status()
    return response.json()["embedding"]