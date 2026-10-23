import os
from dataclasses import dataclass

from google.cloud import speech_v1p1beta1 as speech


@dataclass
class SpeechConfig:
    project_id: str | None = None
    location: str = "us"
    language_code: str = "en-US"


def load_config() -> SpeechConfig:
    return SpeechConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us"),
        language_code=os.getenv("SPEECH_LANGUAGE_CODE", "en-US"),
    )


def get_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def storage_uri(bucket: str, name: str) -> str:
    return f"gs://{bucket}/{name}"
