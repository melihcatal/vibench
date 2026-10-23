import requests

from speech_client import get_client_config, build_headers, build_url, raise_for_api_error
from speech_models import TranscriptionResult


def moderate_transcript(transcript: TranscriptionResult) -> dict:
    config = get_client_config()
    url = build_url(config, "/v1/moderations")
    headers = build_headers(config)
    response = requests.post(url, headers=headers, json={"model": "omni-moderation-latest", "input": transcript.text}, timeout=config.timeout_seconds)
    if response.status_code >= 400:
        raise_for_api_error(response)
    return response.json()
