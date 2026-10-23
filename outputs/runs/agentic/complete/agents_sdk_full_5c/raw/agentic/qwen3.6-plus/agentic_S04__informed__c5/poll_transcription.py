"""
Poll a batch transcription job and return the transcript.

Uses Azure AI Speech batch transcription REST API (v3.1) to check job status
and retrieve the final transcript when the job completes.
"""

import os
import time
import json
from typing import Optional, Tuple

import requests

from speech_client import load_azure_speech_credentials
from speech_models import TranscriptionResult, TranscriptionStatus


def get_auth_headers() -> dict:
    """
    Build HTTP headers with Azure AI Speech subscription key for REST API calls.

    Returns:
        Dictionary of headers including Ocp-Apim-Subscription-Key.
    """
    key, _ = load_azure_speech_credentials()
    return {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }


def poll_transcription_status(
    transcription_id: str,
    max_wait_seconds: int = 3600,
    poll_interval_seconds: int = 15,
) -> Tuple[TranscriptionStatus, dict]:
    """
    Poll an Azure AI Speech batch transcription job until it completes or times out.

    Args:
        transcription_id: The ID of the transcription job returned at submission.
        max_wait_seconds: Maximum seconds to wait before timing out (default 3600).
        poll_interval_seconds: Seconds between each polling attempt (default 15).

    Returns:
        Tuple of (TranscriptionStatus, full response JSON dict).

    Raises:
        RuntimeError: If the transcription job fails or times out.
    """
    _, region = load_azure_speech_credentials()
    base_url = f"https://{region}.api.cognitive.microsoft.com/speechtotext/v3.1"
    endpoint = f"{base_url}/transcriptions/{transcription_id}"
    headers = get_auth_headers()

    elapsed = 0
    while elapsed < max_wait_seconds:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()

        status_str = data.get("status", "notstarted")
        status = TranscriptionStatus.from_string(status_str)

        if status == TranscriptionStatus.SUCCEEDED:
            return status, data
        elif status == TranscriptionStatus.FAILED:
            error_msg = data.get("properties", {}).get("error", {}).get("message", "Unknown error")
            raise RuntimeError(f"Transcription job failed: {error_msg}")

        time.sleep(poll_interval_seconds)
        elapsed += poll_interval_seconds

    raise RuntimeError(
        f"Transcription job polling timed out after {max_wait_seconds} seconds "
        f"(job_id={transcription_id})"
    )


def retrieve_transcription_files(transcription_id: str) -> dict:
    """
    Retrieve the files associated with a completed Azure AI Speech transcription job.

    This includes the primary transcript JSON, detailed results, and any audio logs.

    Args:
        transcription_id: The ID of the completed transcription job.

    Returns:
        Dictionary of file kind -> file URL from the Azure batch API response.

    Raises:
        RuntimeError: If the transcription job has not yet succeeded.
    """
    _, region = load_azure_speech_credentials()
    base_url = f"https://{region}.api.cognitive.microsoft.com/speechtotext/v3.1"
    endpoint = f"{base_url}/transcriptions/{transcription_id}/files"
    headers = get_auth_headers()

    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()

    data = response.json()
    files = {}
    for file_info in data.get("values", []):
        kind = file_info.get("kind", "unknown")
        file_url = file_info.get("links", {}).get("contentUrl")
        if file_url:
            files[kind] = file_url

    return files


def download_transcript_json(file_url: str) -> dict:
    """
    Download the actual transcript JSON content from an Azure Speech blob URL.

    The Azure batch transcription API returns SAS URLs to blob storage containing
    the transcription results. This method downloads and parses the JSON.

    Args:
        file_url: SAS URL to the transcript JSON blob from Azure Speech.

    Returns:
        Parsed JSON dictionary of the transcription result.
    """
    response = requests.get(file_url)
    response.raise_for_status()
    return response.json()


def get_transcription(
    transcription_id: str,
    max_wait_seconds: int = 3600,
    poll_interval_seconds: int = 15,
) -> TranscriptionResult:
    """
    Full workflow: poll for completion and download the transcript.

    Args:
        transcription_id: The transcription job ID.
        max_wait_seconds: Maximum polling duration.
        poll_interval_seconds: Interval between polls.

    Returns:
        TranscriptionResult dataclass with normalized transcript segments.
    """
    status, job_data = poll_transcription_status(
        transcription_id, max_wait_seconds, poll_interval_seconds
    )

    files = retrieve_transcription_files(transcription_id)
    transcript_url = files.get("Transcription")

    if not transcript_url:
        raise RuntimeError("No transcription file URL found in job results")

    raw_data = download_transcript_json(transcript_url)
    return TranscriptionResult.from_azure_response(raw_data)
