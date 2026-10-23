import os
import requests
from typing import Optional


ASSEMBLYAI_API_URL = "https://api.assemblyai.com/v2"


def get_assemblyai_api_key() -> str:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")
    return api_key


def get_assemblyai_headers() -> dict:
    return {
        "authorization": get_assemblyai_api_key(),
        "content-type": "application/json",
    }


def upload_audio_file(file_path: str) -> str:
    api_key = get_assemblyai_api_key()
    headers = {"authorization": api_key}
    with open(file_path, "rb") as f:
        response = requests.post(
            f"{ASSEMBLYAI_API_URL}/upload",
            headers=headers,
            data=f,
        )
    response.raise_for_status()
    return response.json()["upload_url"]


def create_transcription_job(
    audio_url: str,
    speaker_labels: bool = False,
    word_boost: Optional[list[str]] = None,
    custom_spelling: Optional[list[dict]] = None,
    language_code: Optional[str] = None,
    auto_highlights: bool = False,
    content_safety: bool = False,
    iab_categories: bool = False,
    extra_config: Optional[dict] = None,
) -> dict:
    headers = get_assemblyai_headers()
    payload = {
        "audio_url": audio_url,
        "speaker_labels": speaker_labels,
        "auto_highlights": auto_highlights,
        "content_safety": content_safety,
        "iab_categories": iab_categories,
    }
    if word_boost:
        payload["word_boost"] = word_boost
    if custom_spelling:
        payload["custom_spelling"] = custom_spelling
    if language_code:
        payload["language_code"] = language_code
    if extra_config:
        payload.update(extra_config)
    response = requests.post(
        f"{ASSEMBLYAI_API_URL}/transcript",
        headers=headers,
        json=payload,
    )
    response.raise_for_status()
    return response.json()


def get_transcription_result(transcript_id: str) -> dict:
    headers = get_assemblyai_headers()
    response = requests.get(
        f"{ASSEMBLYAI_API_URL}/transcript/{transcript_id}",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()
