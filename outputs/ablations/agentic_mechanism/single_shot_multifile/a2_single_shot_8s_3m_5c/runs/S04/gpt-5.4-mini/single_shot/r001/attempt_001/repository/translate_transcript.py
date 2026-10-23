from typing import List, Optional

import requests

from speech_client import get_client_config, build_headers, build_url, raise_for_api_error
from speech_models import TranscriptionSegment, TranscriptionResult


def translate_transcript(transcript: TranscriptionResult, target_language: str = "en") -> TranscriptionResult:
    config = get_client_config()
    url = build_url(config, "/v1/responses")
    headers = build_headers(config)
    segment_text = "\n".join(segment.text for segment in transcript.segments) if transcript.segments else transcript.text
    payload = {
        "model": "gpt-4o-mini",
        "input": [
            {"role": "system", "content": "Translate transcript text while preserving meaning and speaker markers."},
            {"role": "user", "content": f"Translate to {target_language}:\n{segment_text}"},
        ],
    }
    response = requests.post(url, headers=headers, json=payload, timeout=config.timeout_seconds)
    if response.status_code >= 400:
        raise_for_api_error(response)
    result_text = response.json().get("output_text", "")
    return TranscriptionResult(id=transcript.id, text=result_text, segments=[TranscriptionSegment(text=result_text)], language=target_language)
