import os
from typing import Any, Dict

from google.cloud import speech_v1p1beta1 as speech


def get_speech_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def get_project_id() -> str:
    return os.environ.get("GOOGLE_CLOUD_PROJECT", "")


def build_gcs_uri(bucket: str, object_name: str) -> str:
    return f"gs://{bucket}/{object_name.lstrip('/')}"


def make_long_running_config(language_code: str = "en-US", enable_diarization: bool = False, enable_timestamps: bool = False) -> Dict[str, Any]:
    config = {
        "language_code": language_code,
        "enable_speaker_diarization": enable_diarization,
        "enable_word_time_offsets": enable_timestamps,
        "enable_word_confidence": enable_timestamps,
    }
    return config
