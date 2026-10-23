import os
from typing import Optional

import httpx

ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"
ASSEMBLYAI_LEMUR_BASE = "https://api.assemblyai.com/v2/lemur"


def get_api_key() -> str:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")
    return api_key


def build_headers(api_key: Optional[str] = None) -> dict[str, str]:
    key = api_key or get_api_key()
    return {
        "authorization": key,
        "content-type": "application/json",
    }


def create_client(timeout: float = 30.0) -> httpx.Client:
    return httpx.Client(
        base_url=ASSEMBLYAI_API_BASE,
        headers=build_headers(),
        timeout=timeout,
    )


def create_lemur_client(timeout: float = 30.0) -> httpx.Client:
    return httpx.Client(
        base_url=ASSEMBLYAI_LEMUR_BASE,
        headers=build_headers(),
        timeout=timeout,
    )


def upload_audio_file(file_path: str, api_key: Optional[str] = None) -> str:
    headers = {"authorization": api_key or get_api_key()}
    with open(file_path, "rb") as f:
        response = httpx.post(
            f"{ASSEMBLYAI_API_BASE}/upload",
            headers=headers,
            content=f.read(),
            timeout=300.0,
        )
    response.raise_for_status()
    return response.json()["upload_url"]


def submit_transcription_job(
    audio_url: str,
    language_code: str = "en",
    speaker_labels: bool = False,
    word_timestamps: bool = False,
    punctuate: bool = True,
    format_text: bool = True,
    api_key: Optional[str] = None,
) -> dict:
    headers = build_headers(api_key)
    payload = {
        "audio_url": audio_url,
        "language_code": language_code,
        "speaker_labels": speaker_labels,
        "word_timestamps": word_timestamps,
        "punctuate": punctuate,
        "format_text": format_text,
    }
    response = httpx.post(
        f"{ASSEMBLYAI_API_BASE}/transcript",
        headers=headers,
        json=payload,
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()


def get_transcription_status(transcript_id: str, api_key: Optional[str] = None) -> dict:
    headers = build_headers(api_key)
    response = httpx.get(
        f"{ASSEMBLYAI_API_BASE}/transcript/{transcript_id}",
        headers=headers,
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()


def get_transcription_result(transcript_id: str, api_key: Optional[str] = None) -> dict:
    headers = build_headers(api_key)
    response = httpx.get(
        f"{ASSEMBLYAI_API_BASE}/transcript/{transcript_id}",
        headers=headers,
        timeout=30.0,
    )
    response.raise_for_status()
    return response.json()


def request_lemur_task(
    transcript_ids: list[str],
    prompt: str,
    final_model: str = "assemblyai-mistral-7b",
    max_output_size: int = 2000,
    api_key: Optional[str] = None,
) -> dict:
    headers = build_headers(api_key)
    payload = {
        "transcript_ids": transcript_ids,
        "prompt": prompt,
        "final_model": final_model,
        "max_output_size": max_output_size,
    }
    response = httpx.post(
        f"{ASSEMBLYAI_LEMUR_BASE}/task",
        headers=headers,
        json=payload,
        timeout=60.0,
    )
    response.raise_for_status()
    return response.json()
