import os
from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_TTS_MODEL = os.environ.get("OPENAI_TTS_MODEL", "tts-1")
OPENAI_TTS_HD_MODEL = os.environ.get("OPENAI_TTS_HD_MODEL", "tts-1-hd")
OPENAI_WHISPER_MODEL = os.environ.get("OPENAI_WHISPER_MODEL", "whisper-1")
OPENAI_EMBEDDING_MODEL = os.environ.get(
    "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
)
OPENAI_MODERATION_MODEL = os.environ.get(
    "OPENAI_MODERATION_MODEL", "text-moderation-latest"
)
OPENAI_CHAT_MODEL = os.environ.get("OPENAI_CHAT_MODEL", "gpt-4o-mini")

SUPPORTED_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
SUPPORTED_RESPONSE_FORMATS = ["mp3", "opus", "aac", "flac", "wav", "pcm"]

VOICE_LOCALE_MAP = {
    "alloy": {"locale": "en-US", "gender": "neutral", "accent": "american"},
    "echo": {"locale": "en-US", "gender": "male", "accent": "american"},
    "fable": {"locale": "en-GB", "gender": "male", "accent": "british"},
    "onyx": {"locale": "en-US", "gender": "male", "accent": "american"},
    "nova": {"locale": "en-US", "gender": "female", "accent": "american"},
    "shimmer": {"locale": "en-US", "gender": "female", "accent": "american"},
}


def create_openai_client(
    api_key: str | None = None, base_url: str | None = None
) -> OpenAI:
    key = api_key or OPENAI_API_KEY
    url = base_url or OPENAI_BASE_URL
    return OpenAI(api_key=key, base_url=url)


def get_tts_model(use_hd: bool = False) -> str:
    return OPENAI_TTS_HD_MODEL if use_hd else OPENAI_TTS_MODEL


def validate_voice(voice: str) -> str:
    if voice not in SUPPORTED_VOICES:
        raise ValueError(
            f"Unsupported voice '{voice}'. Choose from: {SUPPORTED_VOICES}"
        )
    return voice


def validate_response_format(fmt: str) -> str:
    if fmt not in SUPPORTED_RESPONSE_FORMATS:
        raise ValueError(
            f"Unsupported format '{fmt}'. Choose from: {SUPPORTED_RESPONSE_FORMATS}"
        )
    return fmt


def find_voice_for_locale(locale: str) -> str:
    locale_lower = locale.lower()
    for voice, info in VOICE_LOCALE_MAP.items():
        if info["locale"].lower() == locale_lower:
            return voice
    if locale_lower.startswith("en"):
        return "alloy"
    raise ValueError(f"No voice found for locale '{locale}'")
