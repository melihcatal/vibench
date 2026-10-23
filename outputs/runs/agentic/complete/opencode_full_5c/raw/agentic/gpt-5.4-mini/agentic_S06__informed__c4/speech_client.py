import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional


def _env(name: str, default: str = '') -> str:
    value = os.getenv(name, default).strip()
    return value


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    region: str
    model: str
    voice: Optional[str]
    output_format: str


@lru_cache(maxsize=1)
def load_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        api_key=_env('AZURE_SPEECH_KEY'),
        region=_env('AZURE_SPEECH_REGION'),
        model=_env('AZURE_SPEECH_TTS_MODEL', 'en-US-JennyNeural'),
        voice=_env('AZURE_SPEECH_VOICE') or None,
        output_format=_env('AZURE_SPEECH_OUTPUT_FORMAT', 'audio-24khz-48kbitrate-mono-mp3'),
    )


def build_endpoint(region: Optional[str] = None) -> str:
    cfg_region = region or load_config().region
    return f'https://{cfg_region}.tts.speech.microsoft.com/cognitiveservices/v1'


def auth_headers() -> dict:
    cfg = load_config()
    return {
        'Ocp-Apim-Subscription-Key': cfg.api_key,
        'X-Microsoft-OutputFormat': cfg.output_format,
        'Content-Type': 'application/ssml+xml',
    }
