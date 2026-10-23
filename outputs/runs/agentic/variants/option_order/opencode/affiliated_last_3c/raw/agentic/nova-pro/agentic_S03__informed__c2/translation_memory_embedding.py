import os
import requests


def embed_translated_segments(text):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    url = "https://dashscope.aliyun.com/api/v1/embeddings"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"input": text}
    response = requests.post(url, headers=headers, json=data)
    return response.json()


if __name__ == "__main__":
    print(embed_translated_segments("This is a translated segment."))
