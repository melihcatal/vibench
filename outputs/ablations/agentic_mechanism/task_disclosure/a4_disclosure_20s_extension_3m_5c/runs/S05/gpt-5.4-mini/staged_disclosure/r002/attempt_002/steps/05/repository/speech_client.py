import os
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Iterator, Optional

import requests


OPENAI_TRANSCRIBE_URL = "https://api.openai.com/v1/audio/transcriptions"
DEFAULT_MODEL = "gpt-4o-mini-transcribe"


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    model: str = DEFAULT_MODEL
    language: Optional[str] = None
    prompt: Optional[str] = None


def load_config(env: Optional[Dict[str, str]] = None) -> SpeechConfig:
    source = env or os.environ
    api_key = source.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    model = source.get("OPENAI_SPEECH_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    language = source.get("OPENAI_SPEECH_LANGUAGE")
    prompt = source.get("OPENAI_SPEECH_PROMPT")
    return SpeechConfig(api_key=api_key, model=model, language=language, prompt=prompt)


def create_headers(api_key: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {api_key}"}


def transcribe_audio(
    audio_file: Any,
    config: Optional[SpeechConfig] = None,
    extra_fields: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    cfg = config or load_config()
    data: Dict[str, Any] = {"model": cfg.model}
    if cfg.language:
        data["language"] = cfg.language
    if cfg.prompt:
        data["prompt"] = cfg.prompt
    if extra_fields:
        data.update(extra_fields)
    files = {"file": audio_file}
    response = requests.post(
        OPENAI_TRANSCRIBE_URL,
        headers=create_headers(cfg.api_key),
        data=data,
        files=files,
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def stream_transcription(
    chunks: Iterable[bytes],
    open_file: Callable[[bytes], Any],
    config: Optional[SpeechConfig] = None,
) -> Iterator[Dict[str, Any]]:
    for chunk in chunks:
        if not chunk:
            continue
        audio_handle = open_file(chunk)
        try:
            yield transcribe_audio(audio_handle, config=config)
        finally:
            close = getattr(audio_handle, "close", None)
            if callable(close):
                close()


def build_streaming_client(env: Optional[Dict[str, str]] = None) -> SpeechConfig:
    return load_config(env=env)
