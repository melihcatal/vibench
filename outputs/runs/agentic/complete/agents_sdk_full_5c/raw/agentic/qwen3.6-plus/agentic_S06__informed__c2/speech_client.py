"""Local helper: configuration and client utilities for Text-to-Speech integrations."""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TTSClientConfig:
    """Configuration for ElevenLabs TTS client."""
    api_key: str = field(default_factory=lambda: os.environ.get("ELEVENLABS_API_KEY", ""))
    voice_id: str = field(default_factory=lambda: os.environ.get("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL"))
    model_id: str = field(default="eleven_multilingual_v2")
    base_url: str = "https://api.elevenlabs.io/v1"
    timeout: int = 30
    max_retries: int = 3


@dataclass
class SSMLClientConfig:
    """Configuration for Azure Speech TTS client."""
    speech_key: str = field(default_factory=lambda: os.environ.get("AZURE_SPEECH_KEY", ""))
    speech_region: str = field(default_factory=lambda: os.environ.get("AZURE_SPEECH_REGION", "eastus"))
    voice_name: str = field(default="en-US-AriaNeural")
    output_format: str = "audio-24khz-48kbitrate-mono-mp3"


@dataclass
class VoiceSelectorConfig:
    """Configuration for Watson TTS voice selection."""
    apikey: str = field(default_factory=lambda: os.environ.get("IBM_TTS_APIKEY", ""))
    url: str = field(default_factory=lambda: os.environ.get("IBM_TTS_URL", "https://api.us-south.text-to-speech.watson.cloud.ibm.com"))
    locale_filter: Optional[str] = None


@dataclass
class AudioSaveConfig:
    """Configuration for Google Cloud TTS audio saving."""
    project_id: str = field(default_factory=lambda: os.environ.get("GOOGLE_CLOUD_PROJECT", ""))
    output_format: str = "MP3"
    sample_rate_hertz: int = 24000
    encoding: str = "MP3"


def get_elevenlabs_api_key() -> str:
    """Retrieve ElevenLabs API key from environment."""
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise EnvironmentError(
            "ELEVENLABS_API_KEY environment variable is required. "
            "Set it to your ElevenLabs API key from https://elevenlabs.io/"
        )
    return key


def get_azure_speech_credentials() -> tuple[str, str]:
    """Retrieve Azure Speech key and region from environment."""
    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION", "eastus")
    if not key:
        raise EnvironmentError(
            "AZURE_SPEECH_KEY environment variable is required. "
            "Set it to your Azure Cognitive Services Speech key."
        )
    return key, region


def get_watson_tts_credentials() -> tuple[str, str]:
    """Retrieve Watson TTS API key and URL from environment."""
    apikey = os.environ.get("IBM_TTS_APIKEY")
    url = os.environ.get("IBM_TTS_URL", "https://api.us-south.text-to-speech.watson.cloud.ibm.com")
    if not apikey:
        raise EnvironmentError(
            "IBM_TTS_APIKEY environment variable is required. "
            "Set it to your IBM Watson Text to Speech API key."
        )
    return apikey, url


def get_google_tts_project() -> str:
    """Retrieve Google Cloud project for TTS."""
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise EnvironmentError(
            "GOOGLE_CLOUD_PROJECT environment variable is required. "
            "Set it to your Google Cloud project ID."
        )
    return project
