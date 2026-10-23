import requests

from speech_client import get_client_config, build_headers, build_url, raise_for_api_error
from speech_models import TranscriptionResult


def archive_summary(transcript: TranscriptionResult, max_tokens: int = 200) -> str:
    config = get_client_config()
    url = build_url(config, "/v1/responses")
    headers = build_headers(config)
    payload = {
        "model": "gpt-4o-mini",
        "input": [
            {"role": "system", "content": "Summarize transcription results for archival storage."},
            {"role": "user", "content": f"Summarize this transcript in under {max_tokens} tokens:\n{transcript.text}"},
        ],
    }
    response = requests.post(url, headers=headers, json=payload, timeout=config.timeout_seconds)
    if response.status_code >= 400:
        raise_for_api_error(response)
    return response.json().get("output_text", "")
