import requests

from speech_client import get_env


def transcript_embedding(segments=None):
    api_key = get_env("COHERE_API_KEY")
    texts = []
    for segment in segments or []:
        if isinstance(segment, dict):
            texts.append(str(segment.get("text", "")))
        else:
            texts.append(str(segment))
    response = requests.post(
        "https://api.cohere.com/v1/embed",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "embed-english-v3.0",
            "texts": texts,
            "input_type": "search_document",
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()
