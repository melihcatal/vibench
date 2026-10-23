import os
import httpx
from typing import Optional

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_TTS_ENDPOINT = "https://api.openai.com/v1/audio/speech"
OPENAI_CHAT_ENDPOINT = "https://api.openai.com/v1/chat/completions"
OPENAI_MODERATIONS_ENDPOINT = "https://api.openai.com/v1/moderations"
OPENAI_EMBEDDINGS_ENDPOINT = "https://api.openai.com/v1/embeddings"
OPENAI_WHISPER_ENDPOINT = "https://api.openai.com/v1/audio/transcriptions"
OPENAI_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
DEFAULT_TTS_MODEL = "tts-1"
DEFAULT_TTS_HD_MODEL = "tts-1-hd"
DEFAULT_CHAT_MODEL = "gpt-4o"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_WHISPER_MODEL = "whisper-1"


def get_openai_headers() -> dict:
    return {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }


def create_http_client(timeout: float = 60.0) -> httpx.Client:
    return httpx.Client(timeout=timeout)


def build_tts_payload(
    model: str = DEFAULT_TTS_MODEL,
    input_text: str = "",
    voice: str = "alloy",
    response_format: str = "mp3",
    speed: float = 1.0,
) -> dict:
    return {
        "model": model,
        "input": input_text,
        "voice": voice,
        "response_format": response_format,
        "speed": speed,
    }


def build_chat_payload(
    messages: list,
    model: str = DEFAULT_CHAT_MODEL,
    temperature: float = 0.0,
) -> dict:
    return {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }


def build_moderation_payload(input_text: str) -> dict:
    return {"input": input_text}


def build_embedding_payload(
    input_text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> dict:
    return {
        "model": model,
        "input": input_text,
    }


def validate_openai_key() -> bool:
    return bool(OPENAI_API_KEY and OPENAI_API_KEY.startswith("sk-"))
