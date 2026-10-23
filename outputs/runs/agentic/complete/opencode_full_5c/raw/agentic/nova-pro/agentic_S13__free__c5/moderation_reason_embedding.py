import requests


def embed_moderation_rationale(text: str) -> str:
    api_key = "YOUR_EMBEDDING_API_KEY"
    api_url = "https://api.embeddingprovider.com/embed"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"text": text}
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["embedding"]
