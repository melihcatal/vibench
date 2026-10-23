import os
import requests
from typing import Optional


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


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

    def read_file(path):
        with open(path, "rb") as f:
            while True:
                data = f.read(5242880)
                if not data:
                    break
                yield data

    response = requests.post(
        f"{ASSEMBLYAI_API_BASE}/upload",
        headers=headers,
        data=read_file(file_path),
    )
    response.raise_for_status()
    return response.json().get("upload_url")


def create_transcription_job(
    audio_url: str,
    language_code: str = "en",
    speaker_labels: bool = False,
    word_timestamps: bool = False,
    auto_highlights: bool = False,
    content_safety: bool = False,
    custom_spelling: Optional[dict] = None,
) -> dict:
    headers = get_assemblyai_headers()
    payload = {
        "audio_url": audio_url,
        "language_code": language_code,
        "speaker_labels": speaker_labels,
        "word_timestamps": word_timestamps,
        "auto_highlights": auto_highlights,
        "content_safety": content_safety,
    }
    if custom_spelling:
        payload["custom_spelling"] = custom_spelling

    response = requests.post(
        f"{ASSEMBLYAI_API_BASE}/transcript",
        json=payload,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


def get_transcription_status(job_id: str) -> dict:
    headers = get_assemblyai_headers()
    response = requests.get(
        f"{ASSEMBLYAI_API_BASE}/transcript/{job_id}",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


def get_transcription_result(job_id: str) -> dict:
    return get_transcription_status(job_id)
