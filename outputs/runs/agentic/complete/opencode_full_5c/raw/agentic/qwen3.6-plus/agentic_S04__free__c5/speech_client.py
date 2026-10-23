import os
from typing import Optional
import httpx

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_ORGANIZATION = os.environ.get("OPENAI_ORGANIZATION", "")

BATCH_ENDPOINT = f"{OPENAI_BASE_URL}/batches"
FILES_ENDPOINT = f"{OPENAI_BASE_URL}/files"
TRANSCRIPTION_ENDPOINT = f"{OPENAI_BASE_URL}/audio/transcriptions"
TRANSLATION_ENDPOINT = f"{OPENAI_BASE_URL}/audio/translations"
MODERATION_ENDPOINT = f"{OPENAI_BASE_URL}/moderations"
CHAT_ENDPOINT = f"{OPENAI_BASE_URL}/chat/completions"
EMBEDDINGS_ENDPOINT = f"{OPENAI_BASE_URL}/embeddings"

DEFAULT_MODEL = "whisper-1"
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"


def get_headers() -> dict:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    if OPENAI_ORGANIZATION:
        headers["OpenAI-Organization"] = OPENAI_ORGANIZATION
    return headers


def get_sync_client(timeout: float = 60.0) -> httpx.Client:
    return httpx.Client(
        base_url=OPENAI_BASE_URL,
        headers=get_headers(),
        timeout=timeout,
    )


def get_async_client(timeout: float = 60.0) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=OPENAI_BASE_URL,
        headers=get_headers(),
        timeout=timeout,
    )


def validate_api_key() -> bool:
    return bool(OPENAI_API_KEY and OPENAI_API_KEY.startswith("sk-"))


def build_audio_payload(
    audio_file_path: str,
    model: str = DEFAULT_MODEL,
    response_format: str = "verbose_json",
    language: Optional[str] = None,
    temperature: float = 0.0,
    timestamp_granularities: Optional[list] = None,
) -> dict:
    payload = {
        "model": model,
        "response_format": response_format,
        "temperature": temperature,
    }
    if language:
        payload["language"] = language
    if timestamp_granularities:
        payload["timestamp_granularities[]"] = timestamp_granularities
    return payload


def build_batch_payload(
    input_file_id: str,
    endpoint: str = "/v1/audio/transcriptions",
    completion_window: str = "24h",
) -> dict:
    return {
        "input_file_id": input_file_id,
        "endpoint": endpoint,
        "completion_window": completion_window,
    }


def parse_verbose_json_response(response_data: dict) -> dict:
    return {
        "text": response_data.get("text", ""),
        "language": response_data.get("language", ""),
        "duration": response_data.get("duration", 0.0),
        "segments": response_data.get("segments", []),
        "words": response_data.get("words", []),
    }


def extract_segments_from_response(response_data: dict) -> list:
    segments = response_data.get("segments", [])
    result = []
    for seg in segments:
        result.append(
            {
                "id": seg.get("id", 0),
                "start": seg.get("start", 0.0),
                "end": seg.get("end", 0.0),
                "text": seg.get("text", "").strip(),
                "tokens": seg.get("tokens", []),
                "temperature": seg.get("temperature", 0.0),
                "avg_logprob": seg.get("avg_logprob", 0.0),
                "compression_ratio": seg.get("compression_ratio", 0.0),
                "no_speech_prob": seg.get("no_speech_prob", 0.0),
            }
        )
    return result


def extract_words_from_response(response_data: dict) -> list:
    words = response_data.get("words", [])
    result = []
    for word in words:
        result.append(
            {
                "word": word.get("word", ""),
                "start": word.get("start", 0.0),
                "end": word.get("end", 0.0),
            }
        )
    return result
