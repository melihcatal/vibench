"""
Local configuration and client helper utilities for Batch Speech-to-Text
using AssemblyAI API.
"""

import os
from typing import Optional

import requests


ASSEMBLYAI_API_URL = "https://api.assemblyai.com/v2"
ASSEMBLYAI_UPLOAD_ENDPOINT = f"{ASSEMBLYAI_API_URL}/upload"
ASSEMBLYAI_TRANSCRIPTION_ENDPOINT = f"{ASSEMBLYAI_API_URL}/transcript"


def get_api_key() -> str:
    """Retrieve AssemblyAI API key from environment."""
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")
    return api_key


def get_headers() -> dict:
    """Build AssemblyAI authorization headers."""
    return {
        "authorization": get_api_key(),
        "content-type": "application/json",
    }


def upload_audio_file(audio_path: str) -> str:
    """
    Upload an audio file to AssemblyAI and return the hosted audio URL.
    """
    headers = {"authorization": get_api_key()}
    with open(audio_path, "rb") as f:
        response = requests.post(
            ASSEMBLYAI_UPLOAD_ENDPOINT,
            headers=headers,
            data=f,
        )
    response.raise_for_status()
    return response.json()["upload_url"]


def create_transcription_request(
    audio_url: str,
    **kwargs,
) -> dict:
    """
    Build a transcription submission payload for AssemblyAI.

    Parameters
    ----------
    audio_url : str
        URL of the audio file to transcribe.
    **kwargs : dict
        Optional transcription options:
        - speaker_labels (bool): Enable speaker diarization
        - word_timestamps (bool): Enable word-level timestamps
        - language_code (str): Language code (e.g., 'en', 'es', 'fr')
        - punctuate (bool): Enable automatic punctuation
        - format_text (bool): Enable text formatting
    """
    payload = {"audio_url": audio_url}

    if "speaker_labels" in kwargs:
        payload["speaker_labels"] = kwargs["speaker_labels"]
    if "word_timestamps" in kwargs:
        payload["word_timestamps"] = kwargs["word_timestamps"]
    if "language_code" in kwargs:
        payload["language_code"] = kwargs["language_code"]
    if "punctuate" in kwargs:
        payload["punctuate"] = kwargs["punctuate"]
    if "format_text" in kwargs:
        payload["format_text"] = kwargs["format_text"]

    return payload


def submit_transcription_job(payload: dict) -> str:
    """
    Submit a transcription job to AssemblyAI and return the job ID.
    """
    response = requests.post(
        ASSEMBLYAI_TRANSCRIPTION_ENDPOINT,
        headers=get_headers(),
        json=payload,
    )
    response.raise_for_status()
    return response.json()["id"]


def get_transcription_status(job_id: str) -> dict:
    """
    Retrieve the status and results of a transcription job from AssemblyAI.
    """
    url = f"{ASSEMBLYAI_TRANSCRIPTION_ENDPOINT}/{job_id}"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()


def wait_for_completion(
    job_id: str,
    poll_interval: float = 3.0,
    timeout: float = 300.0,
) -> dict:
    """
    Poll AssemblyAI until the transcription job completes or times out.
    """
    import time

    start = time.time()
    while time.time() - start < timeout:
        result = get_transcription_status(job_id)
        status = result.get("status")
        if status == "completed":
            return result
        if status == "error":
            raise RuntimeError(f"Transcription failed: {result.get('error')}")
        time.sleep(poll_interval)

    raise TimeoutError(f"Transcription job {job_id} did not complete within {timeout}s")
