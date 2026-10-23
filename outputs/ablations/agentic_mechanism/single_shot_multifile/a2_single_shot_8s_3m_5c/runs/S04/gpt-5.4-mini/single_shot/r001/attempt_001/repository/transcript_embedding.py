import requests

from speech_client import get_client_config, build_headers, build_url, raise_for_api_error
from speech_models import TranscriptionResult


def transcript_embedding(transcript: TranscriptionResult) -> list:
    config = get_client_config()
    url = build_url(config, "/v1/embeddings")
    headers = build_headers(config)
    response = requests.post(url, headers=headers, json={"model": "text-embedding-3-large", "input": transcript.text}, timeout=config.timeout_seconds)
    if response.status_code >= 400:
        raise_for_api_error(response)
    data = response.json().get("data", [])
    return data[0].get("embedding", []) if data else []
