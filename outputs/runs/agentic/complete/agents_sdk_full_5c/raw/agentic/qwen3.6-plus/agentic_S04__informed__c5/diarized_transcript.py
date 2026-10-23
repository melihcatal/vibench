"""
Request speaker diarization for a recorded meeting using Azure AI Speech.

Submits a batch transcription job with diarization enabled, waits for completion,
and returns a transcript with speaker labels for each segment.
"""

import os
import json
import time
from typing import List, Optional, Tuple

import requests

from speech_client import get_default_batch_endpoint, load_azure_speech_credentials
from speech_models import (
    TranscriptionResult,
    TranscriptionSegment,
    TranscriptionStatus,
    SpeakerDiarizationResult,
)


def submit_diarized_transcription(
    audio_uri: str,
    locale: str = "en-US",
    display_name: str = "meeting_diarization",
    model_id: Optional[str] = None,
) -> str:
    """
    Submit an audio file for batch transcription with speaker diarization
    enabled via the Azure AI Speech batch transcription REST API.

    Args:
        audio_uri: Accessible URI (SAS or public) to the meeting audio file.
        locale: Language locale for the speech recognition.
        display_name: Display name for this transcription job.
        model_id: Optional Azure Speech model ID to use.

    Returns:
        The transcription job ID from Azure AI Speech.
    """
    key, region = load_azure_speech_credentials()
    endpoint = f"https://{region}.api.cognitive.microsoft.com/speechtotext/v3.1/transcriptions"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    properties = {
        "diarizationEnabled": True,
        "wordLevelTimestampsEnabled": True,
        "punctuationMode": "dictated_and_automatic",
        "profanityFilterMode": "masked",
    }

    payload = {
        "displayName": display_name,
        "locale": locale,
        "recordingsUrl": audio_uri,
        "properties": properties,
    }

    if model_id:
        payload["models"] = [{"id": model_id}]

    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()

    location = response.headers.get("location", "")
    transcription_id = location.rstrip("/").split("/")[-1]
    return transcription_id


def wait_for_diarized_completion(
    transcription_id: str,
    max_wait_seconds: int = 3600,
    poll_interval_seconds: int = 15,
) -> dict:
    """
    Wait for a diarized transcription job to complete on Azure AI Speech.

    Args:
        transcription_id: The job ID returned from submission.
        max_wait_seconds: Maximum wait time.
        poll_interval_seconds: Polling interval.

    Returns:
        The raw job status response JSON.

    Raises:
        RuntimeError: If the job fails or times out.
    """
    _, region = load_azure_speech_credentials()
    status_endpoint = f"https://{region}.api.cognitive.microsoft.com/speechtotext/v3.1/transcriptions/{transcription_id}"

    headers = {
        "Ocp-Apim-Subscription-Key": region,
    }

    elapsed = 0
    while elapsed < max_wait_seconds:
        resp = requests.get(status_endpoint, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        status = data.get("status", "")
        if status == "Succeeded":
            return data
        elif status == "Failed":
            error_msg = data.get("properties", {}).get("error", {}).get("message", "Unknown")
            raise RuntimeError(f"Diarized transcription failed: {error_msg}")

        time.sleep(poll_interval_seconds)
        elapsed += poll_interval_seconds

    raise RuntimeError(
        f"Diarized transcription timed out after {max_wait_seconds}s (job: {transcription_id})"
    )


def get_diarized_files(transcription_id: str) -> dict:
    """
    Retrieve file URLs for a completed diarized transcription job.

    Args:
        transcription_id: The completed job ID.

    Returns:
        Dict mapping file kind to its download URL.
    """
    _, region = load_azure_speech_credentials()
    files_endpoint = f"https://{region}.api.cognitive.microsoft.com/speechtotext/v3.1/transcriptions/{transcription_id}/files"

    headers = {
        "Ocp-Apim-Subscription-Key": region,
    }

    resp = requests.get(files_endpoint, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    files = {}
    for file_info in data.get("values", []):
        kind = file_info.get("kind", "unknown")
        url = file_info.get("links", {}).get("contentUrl")
        if url:
            files[kind] = url

    return files


def download_diarized_results(file_url: str) -> dict:
    """
    Download diarized transcription JSON from Azure blob storage.

    Args:
        file_url: SAS URL to the transcription JSON blob.

    Returns:
        Parsed JSON with Azure AI Speech diarization output.
    """
    resp = requests.get(file_url)
    resp.raise_for_status()
    return resp.json()


def extract_speaker_segments(raw_result: dict) -> SpeakerDiarizationResult:
    """
    Extract speaker-labeled segments from Azure AI Speech batch transcription output.

    Azure AI Speech batch transcription with diarization returns a combinedPhrases
    list where each entry has a speaker tag.

    Args:
        raw_result: The downloaded JSON from the transcription file.

    Returns:
        SpeakerDiarizationResult with normalized speaker segments.
    """
    combined_phrases = raw_result.get("combinedPhrases", [])

    segments: List[TranscriptionSegment] = []
    for phrase in combined_phrases:
        speaker = phrase.get("speaker", "Unknown")
        text = phrase.get("text", "")
        offset = phrase.get("offset", 0)
        duration = phrase.get("duration", 0)

        segments.append(
            TranscriptionSegment(
                text=text,
                speaker_label=speaker,
                start_time_ms=offset,
                end_time_ms=offset + duration,
            )
        )

    return SpeakerDiarizationResult(
        segments=segments,
        speaker_count=len(set(s.speaker_label for s in segments if s.speaker_label != "Unknown")),
    )


def get_diarized_transcript(
    audio_uri: str,
    locale: str = "en-US",
    display_name: str = "meeting_diarization",
    max_wait_seconds: int = 3600,
) -> SpeakerDiarizationResult:
    """
    Full workflow: submit diarized transcription, wait, and return speaker-labeled segments.

    Args:
        audio_uri: URI to the meeting audio.
        locale: Language locale.
        display_name: Job display name.
        max_wait_seconds: Max wait time for job completion.

    Returns:
        SpeakerDiarizationResult with segments labeled by speaker.
    """
    job_id = submit_diarized_transcription(
        audio_uri=audio_uri, locale=locale, display_name=display_name
    )

    wait_for_diarized_completion(job_id, max_wait_seconds=max_wait_seconds)
    files = get_diarized_files(job_id)

    transcription_url = files.get("Transcription")
    if not transcription_url:
        raise RuntimeError("No transcription file found for diarized job")

    raw_result = download_diarized_results(transcription_url)
    return extract_speaker_segments(raw_result)
