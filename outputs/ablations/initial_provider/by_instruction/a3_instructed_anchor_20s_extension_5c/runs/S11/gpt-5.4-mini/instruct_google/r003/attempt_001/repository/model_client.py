import os
from dataclasses import dataclass
from typing import Optional

from google import genai


@dataclass
class PlatformConfig:
    project: Optional[str]
    location: Optional[str]
    model: str


def load_platform_config() -> PlatformConfig:
    return PlatformConfig(
        project=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION") or os.getenv("GOOGLE_GENAI_LOCATION") or "us-central1",
        model=os.getenv("GOOGLE_GENAI_MODEL", "gemini-2.0-flash"),
    )


def create_client() -> genai.Client:
    return genai.Client(vertexai=True, project=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT"), location=os.getenv("GOOGLE_CLOUD_LOCATION") or os.getenv("GOOGLE_GENAI_LOCATION") or "us-central1")
