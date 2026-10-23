"""
Local configuration and client helper utilities for Streaming Speech-to-Text.

Provides credential loading, client instantiation for Google Cloud Speech-to-Text,
and shared configuration constants used across the streaming speech integration.
"""

import logging
import os
from dataclasses import dataclass, field

from google.cloud.speech_v1 import SpeechClient
from google.cloud.speech_v1.types import (
    RecognitionConfig,
    StreamingRecognitionConfig,
)

logger = logging.getLogger(__name__)

GOOGLE_CLOUD_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"
GOOGLE_APPLICATION_CREDENTIALS_ENV = "GOOGLE_APPLICATION_CREDENTIALS"
GOOGLE_CLOUD_SPEECH_API_ENDPOINT = "speech.googleapis.com"


@dataclass
class SpeechConfig:
    """Configuration for Google Cloud Speech-to-Text streaming operations."""
    project_id: str = ""
    language_code: str = "en-US"
    alternative_language_codes: list[str] = field(default_factory=list)
    sample_rate_hertz: int = 16000
    model: str = "latest_long"
    enable_automatic_punctuation: bool = True
    enable_word_time_offsets: bool = True
    profanity_filter: bool = False
    use_enhanced: bool = True
    max_alternatives: int = 1
    audio_encoding: str = "LINEAR16"


def load_project_id() -> str:
    """Load the Google Cloud project ID from environment or metadata."""
    project_id = os.environ.get(GOOGLE_CLOUD_PROJECT_ENV, "")
    if not project_id:
        logger.warning(
            "%s not set; using default project lookup",
            GOOGLE_CLOUD_PROJECT_ENV,
        )
    return project_id


def validate_credentials() -> bool:
    """Check that Google Cloud credentials are available."""
    credentials_path = os.environ.get(GOOGLE_APPLICATION_CREDENTIALS_ENV)
    if credentials_path and os.path.isfile(credentials_path):
        logger.info("Google Cloud credentials found at: %s", credentials_path)
        return True
    logger.warning(
        "%s not set or file not found; relying on default credential chain",
        GOOGLE_APPLICATION_CREDENTIALS_ENV,
    )
    return False


def create_speech_client() -> SpeechClient:
    """
    Create and return a Google Cloud SpeechClient instance.

    Uses the GOOGLE_APPLICATION_CREDENTIALS environment variable for
    authentication if available, falling back to the default credential chain.
    """
    validate_credentials()
    project_id = load_project_id()

    client_kwargs = {}
    if project_id:
        logger.info("Initializing SpeechClient for project: %s", project_id)

    client = SpeechClient(**client_kwargs)
    logger.info(
        "Google Cloud SpeechClient connected to %s",
        GOOGLE_CLOUD_SPEECH_API_ENDPOINT,
    )
    return client


def build_recognition_config(config: SpeechConfig) -> RecognitionConfig:
    """
    Build a Google Cloud RecognitionConfig from SpeechConfig.
    """
    encoding_map = {
        "LINEAR16": RecognitionConfig.AudioEncoding.LINEAR16,
        "FLAC": RecognitionConfig.AudioEncoding.FLAC,
        "MULAW": RecognitionConfig.AudioEncoding.MULAW,
        "AMR": RecognitionConfig.AudioEncoding.AMR,
        "AMR_WB": RecognitionConfig.AudioEncoding.AMR_WB,
        "OGG_OPUS": RecognitionConfig.AudioEncoding.OGG_OPUS,
        "SPEEX_WITH_HEADER_BYTE": RecognitionConfig.AudioEncoding.SPEEX_WITH_HEADER_BYTE,
    }

    encoding = encoding_map.get(config.audio_encoding, RecognitionConfig.AudioEncoding.LINEAR16)

    kwargs = {
        "model": config.model,
        "language_code": config.language_code,
        "sample_rate_hertz": config.sample_rate_hertz,
        "enable_automatic_punctuation": config.enable_automatic_punctuation,
        "enable_word_time_offsets": config.enable_word_time_offsets,
        "profanity_filter": config.profanity_filter,
        "use_enhanced": config.use_enhanced,
        "max_alternatives": config.max_alternatives,
        "encoding": encoding,
    }

    if config.alternative_language_codes:
        kwargs["alternative_language_codes"] = config.alternative_language_codes

    return RecognitionConfig(**kwargs)


def build_streaming_config(config: SpeechConfig, interim_results: bool = True) -> StreamingRecognitionConfig:
    """
    Build a Google Cloud StreamingRecognitionConfig from SpeechConfig.
    """
    recognition_config = build_recognition_config(config)
    return StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=interim_results,
        single_utterance=False,
    )


def get_default_config() -> SpeechConfig:
    """Return a default SpeechConfig for Google Cloud Speech-to-Text."""
    return SpeechConfig(
        project_id=load_project_id(),
    )
