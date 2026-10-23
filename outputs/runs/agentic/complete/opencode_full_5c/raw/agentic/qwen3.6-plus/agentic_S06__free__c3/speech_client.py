import os
from openai import OpenAI


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key, base_url="https://api.openai.com/v1")


def load_tts_config() -> dict:
    return {
        "default_model": os.environ.get("TTS_MODEL", "tts-1"),
        "default_voice": os.environ.get("TTS_VOICE", "alloy"),
        "default_format": os.environ.get("TTS_FORMAT", "mp3"),
        "default_speed": float(os.environ.get("TTS_SPEED", "1.0")),
        "api_base": "https://api.openai.com/v1",
    }
