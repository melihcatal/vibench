"""
Local configuration and client helper utilities for Batch Speech-to-Text.

Provider: Google Cloud Speech-to-Text API
SDK: google-cloud-speech
Hostname: speech.googleapis.com
Environment: GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT
"""

import os
import time
import json
from typing import Optional, Dict, Any

from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech


GOOGLE_SPEECH_ENDPOINT = "speech.googleapis.com"
GOOGLE_SPEECH_REGION = "us-central1"


def get_speech_client(
    project_id: Optional[str] = None,
    region: str = GOOGLE_SPEECH_REGION,
) -> speech_v2.SpeechClient:
    """
    Create and return a configured Google Cloud Speech-to-Text v2 client.

    Requires GOOGLE_APPLICATION_CREDENTIALS to be set for service account authentication.
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT environment variable is not set"
            )

    client = speech_v2.SpeechClient()
    return client


def get_project_path(project_id: Optional[str] = None) -> str:
    """Build the Google Cloud project resource path for Speech-to-Text."""
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT environment variable is not set"
            )
    return f"projects/{project_id}/locations/{GOOGLE_SPEECH_REGION}"


def build_recognizer(
    client: speech_v2.SpeechClient,
    project_id: Optional[str] = None,
    language_code: str = "en-US",
    model: str = "long",
    enable_diarization: bool = False,
    enable_word_time_offsets: bool = False,
) -> str:
    """
    Create or retrieve a Recognizer resource in Google Cloud Speech-to-Text.

    Returns the recognizer resource name.
    """
    parent = get_project_path(project_id)
    recognizer_id = "batch-recognizer"

    try:
        recognizer_request = cloud_speech.GetRecognizerRequest(
            name=f"{parent}/recognizers/{recognizer_id}",
        )
        recognizer = client.get_recognizer(request=recognizer_request)
        return recognizer.name
    except Exception:
        pass

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[language_code],
        model=model,
        features=cloud_speech.RecognitionFeatures(
            enable_automatic_punctuation=True,
            enable_word_time_offsets=enable_word_time_offsets,
            enable_speaker_diarization=enable_diarization,
            diarization_config=cloud_speech.SpeakerDiarizationConfig(
                min_speaker_count=2,
                max_speaker_count=6,
            ) if enable_diarization else None,
        ),
    )

    create_request = cloud_speech.CreateRecognizerRequest(
        parent=parent,
        recognizer_id=recognizer_id,
        recognizer=cloud_speech.Recognizer(
            language_codes=[language_code],
            config=config,
        ),
    )

    operation = client.create_recognizer(request=create_request)
    recognizer = operation.result(timeout=300)
    return recognizer.name


def build_audio_input_from_gcs(
    gcs_uri: str,
) -> cloud_speech.BatchRecognizeFileMetadata:
    """
    Build a BatchRecognizeFileMetadata pointing to a GCS audio file.

    Provider: Google Cloud Storage (storage.googleapis.com)
    """
    return cloud_speech.BatchRecognizeFileMetadata(
        uri=gcs_uri,
    )


def wait_for_operation(operation, timeout: int = 600, poll_interval: int = 10) -> Any:
    """Poll a long-running operation until completion."""
    start = time.time()
    while not operation.done():
        elapsed = time.time() - start
        if elapsed > timeout:
            raise TimeoutError(
                f"Operation did not complete within {timeout} seconds"
            )
        time.sleep(poll_interval)
    return operation.result()


def parse_recognition_results(results) -> Dict[str, Any]:
    """
    Parse Google Cloud Speech-to-Text batch recognition results into
    a normalized dictionary structure.
    """
    normalized = {
        "results": [],
        "total_segments": 0,
        "has_diarization": False,
        "has_word_timestamps": False,
    }

    for result in results:
        for alternative in result.alternatives:
            segment = {
                "transcript": alternative.transcript,
                "confidence": alternative.confidence,
                "words": [],
                "speaker_tag": None,
            }

            if alternative.words:
                normalized["has_word_timestamps"] = True
                for word_info in alternative.words:
                    word_entry = {
                        "word": word_info.word,
                        "start_offset_seconds": word_info.start_offset.seconds
                            + word_info.start_offset.microseconds / 1_000_000,
                        "end_offset_seconds": word_info.end_offset.seconds
                            + word_info.end_offset.microseconds / 1_000_000,
                    }
                    if hasattr(word_info, "speaker_tag") and word_info.speaker_tag:
                        word_entry["speaker_tag"] = word_info.speaker_tag
                        normalized["has_diarization"] = True
                    segment["words"].append(word_entry)

            if hasattr(result, "language_code") and result.language_code:
                segment["language_code"] = result.language_code

            normalized["results"].append(segment)
            normalized["total_segments"] += 1

    return normalized
