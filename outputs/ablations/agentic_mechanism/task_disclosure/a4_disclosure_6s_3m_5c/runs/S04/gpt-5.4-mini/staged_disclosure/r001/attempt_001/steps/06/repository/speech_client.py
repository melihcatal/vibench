import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from openai import OpenAI

OPENAI_BATCH_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_BATCH_BASE_URL = "https://api.openai.com/v1"
OPENAI_BATCH_MODEL = "gpt-4o-mini-transcribe"
OPENAI_BATCH_ENDPOINT = "/v1/audio/transcriptions"


@dataclass(frozen=True)
class BatchSpeechConfig:
    api_key: str
    base_url: str = OPENAI_BATCH_BASE_URL
    model: str = OPENAI_BATCH_MODEL


def load_batch_speech_config() -> BatchSpeechConfig:
    api_key = os.getenv(OPENAI_BATCH_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"{OPENAI_BATCH_API_KEY_ENV} is required")
    return BatchSpeechConfig(api_key=api_key)


def create_batch_speech_client(config: Optional[BatchSpeechConfig] = None) -> OpenAI:
    cfg = config or load_batch_speech_config()
    return OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)


def transcribe_audio_file(
    audio_path: str | Path,
    *,
    timestamp_granularities: Optional[Iterable[str]] = None,
    response_format: str = "verbose_json",
    model: Optional[str] = None,
    config: Optional[BatchSpeechConfig] = None,
) -> Dict[str, Any]:
    cfg = config or load_batch_speech_config()
    client = create_batch_speech_client(cfg)
    with Path(audio_path).open("rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=model or cfg.model,
            file=audio_file,
            response_format=response_format,
            timestamp_granularities=list(timestamp_granularities) if timestamp_granularities is not None else ["word", "segment"],
        )
    if hasattr(response, "model_dump"):
        return response.model_dump()
    return dict(response)


def extract_transcript(result: Dict[str, Any]) -> str:
    if "text" in result and isinstance(result["text"], str):
        return result["text"]
    if "transcript" in result and isinstance(result["transcript"], str):
        return result["transcript"]
    response = result.get("response")
    if isinstance(response, dict):
        body = response.get("body")
        if isinstance(body, dict):
            text = body.get("text")
            if isinstance(text, str):
                return text
            transcript = body.get("transcript")
            if isinstance(transcript, str):
                return transcript
    return ""


def get_timestamps(result: Dict[str, Any]) -> Dict[str, list[Dict[str, Any]]]:
    return {"words": list(result.get("words") or []), "segments": list(result.get("segments") or [])}
