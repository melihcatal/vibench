import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_TTS_MODEL = os.getenv("OPENAI_TTS_MODEL", "tts-1")
OPENAI_TTS_HD_MODEL = os.getenv("OPENAI_TTS_HD_MODEL", "tts-1-hd")

DEFAULT_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
DEFAULT_VOICE = os.getenv("OPENAI_TTS_VOICE", "alloy")
DEFAULT_RESPONSE_FORMAT = os.getenv("OPENAI_TTS_FORMAT", "mp3")
DEFAULT_SPEED = float(os.getenv("OPENAI_TTS_SPEED", "1.0"))

_client = None


def get_openai_client():
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=OPENAI_API_KEY,
            base_url=OPENAI_BASE_URL,
        )
    return _client


def reset_client():
    global _client
    _client = None


def get_tts_model(hd=False):
    return OPENAI_TTS_HD_MODEL if hd else OPENAI_TTS_MODEL


def validate_voice(voice):
    if voice not in DEFAULT_VOICES:
        raise ValueError(
            f"Invalid OpenAI voice: {voice}. Must be one of {DEFAULT_VOICES}"
        )
    return voice


def validate_speed(speed):
    speed = float(speed)
    if speed < 0.25 or speed > 4.0:
        raise ValueError(f"OpenAI TTS speed must be between 0.25 and 4.0, got {speed}")
    return speed


def validate_format(fmt):
    valid_formats = ["mp3", "opus", "aac", "flac", "wav", "pcm"]
    if fmt not in valid_formats:
        raise ValueError(
            f"Invalid OpenAI TTS format: {fmt}. Must be one of {valid_formats}"
        )
    return fmt
