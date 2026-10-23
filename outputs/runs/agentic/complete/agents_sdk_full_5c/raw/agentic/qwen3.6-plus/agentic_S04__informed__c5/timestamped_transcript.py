"""
Return word or segment timestamps from a transcription result.

Uses Azure AI Speech batch transcription API to retrieve detailed
word-level timing information from completed transcription jobs.
"""

import os
import json
import time
from typing import List, Optional, Dict

import requests

from speech_client import load_azure_speech_credentials
from speech_models import (
    TimestampedWord,
    TimestampedSegment,
    TimestampedTranscript,
)


def get_timestamped_files(transcription_id: str) -> Dict[str, str]:
    """
    Retrieve file URLs for a completed Azure AI Speech transcription job.

    The Azure batch API returns URLs to different file kinds including
    the detailed JSON that contains word-level timing data.

    Args:
        transcription_id: The completed job ID.

    Returns:
        Dictionary mapping file kind to download URL.
    """
    _, region = load_azure_speech_credentials()
    endpoint = f"https://{region}.api.cognitive.microsoft.com/speechtotext/v3.1/transcriptions/{transcription_id}/files"

    headers = {
        "Ocp-Apim-Subscription-Key": region,
    }

    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()

    data = response.json()
    files = {}
    for file_info in data.get("values", []):
        kind = file_info.get("kind", "unknown")
        url = file_info.get("links", {}).get("contentUrl")
        if url:
            files[kind] = url

    return files


def download_timestamped_json(file_url: str) -> dict:
    """
    Download the detailed transcription JSON from Azure blob storage.

    The JSON contains the 'recognizedPhrases' array with word-level
    'nBest' entries that include individual word timestamps.

    Args:
        file_url: SAS URL to the transcription result blob.

    Returns:
        Parsed JSON from the Azure AI Speech transcription file.
    """
    response = requests.get(file_url)
    response.raise_for_status()
    return response.json()


def extract_word_timestamps(raw_result: dict) -> List[TimestampedWord]:
    """
    Extract word-level timestamps from Azure AI Speech batch transcription output.

    Azure AI Speech returns word timing in the 'nBest' array with each word
    having offset and duration properties measured in 100-nanosecond units.

    Args:
        raw_result: The detailed transcription JSON from Azure.

    Returns:
        List of TimestampedWord objects with normalized timing.
    """
    words = []
    recognized_phrases = raw_result.get("recognizedPhrases", [])

    for phrase in recognized_phrases:
        n_best = phrase.get("nBest", [])
        if not n_best:
            continue

        best_hypothesis = n_best[0]
        display = best_hypothesis.get("display", "")

        for word_info in best_hypothesis.get("words", []):
            word_text = word_info.get("word", "")
            offset = word_info.get("offset", 0)
            duration = word_info.get("duration", 0)

            confidence = word_info.get("confidence", 0.0)

            # Azure Speech uses 100-nanosecond units, convert to milliseconds
            start_ms = offset / 10000
            end_ms = (offset + duration) / 10000

            words.append(
                TimestampedWord(
                    text=word_text,
                    start_time_ms=start_ms,
                    end_time_ms=end_ms,
                    confidence=confidence,
                )
            )

    return words


def extract_segment_timestamps(raw_result: dict) -> List[TimestampedSegment]:
    """
    Extract phrase/segment-level timestamps from Azure AI Speech output.

    Groups word-level data into segments based on phrase boundaries
    with start/end times for each recognized segment.

    Args:
        raw_result: The detailed transcription JSON from Azure.

    Returns:
        List of TimestampedSegment objects.
    """
    segments = []
    recognized_phrases = raw_result.get("recognizedPhrases", [])

    for phrase in recognized_phrases:
        phrase_offset = phrase.get("offset", 0)
        phrase_duration = phrase.get("duration", 0)

        # Convert from 100ns units to ms
        start_ms = phrase_offset / 10000
        end_ms = (phrase_offset + phrase_duration) / 10000

        n_best = phrase.get("nBest", [])
        display = ""
        words_in_segment = []

        if n_best:
            display = n_best[0].get("display", "")
            for word_info in n_best[0].get("words", []):
                word_offset = word_info.get("offset", 0)
                word_duration = word_info.get("duration", 0)
                words_in_segment.append(
                    TimestampedWord(
                        text=word_info.get("word", ""),
                        start_time_ms=word_offset / 10000,
                        end_time_ms=(word_offset + word_duration) / 10000,
                        confidence=word_info.get("confidence", 0.0),
                    )
                )

        segments.append(
            TimestampedSegment(
                text=display,
                start_time_ms=start_ms,
                end_time_ms=end_ms,
                words=words_in_segment,
            )
        )

    return segments


def get_timestamped_transcript(
    transcription_id: str,
) -> TimestampedTranscript:
    """
    Full workflow: retrieve and parse word/segment timestamps from a completed job.

    Downloads the detailed JSON from Azure AI Speech batch transcription
    and extracts both word-level and segment-level timing information.

    Args:
        transcription_id: The completed Azure transcription job ID.

    Returns:
        TimestampedTranscript with words and segments.

    Raises:
        RuntimeError: If no detailed transcription file is available.
    """
    files = get_timestamped_files(transcription_id)
    transcription_url = files.get("Transcription")

    if not transcription_url:
        raise RuntimeError(
            "No transcription file URL available for timestamp extraction"
        )

    raw_result = download_timestamped_json(transcription_url)

    words = extract_word_timestamps(raw_result)
    segments = extract_segment_timestamps(raw_result)

    return TimestampedTranscript(
        words=words,
        segments=segments,
        total_duration_ms=segments[-1].end_time_ms if segments else 0,
    )
