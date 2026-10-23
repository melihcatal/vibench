import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass(frozen=True)
class BatchSpeechConfig:
    api_key: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None
    base_url: Optional[str] = None
    model: str = "gpt-4o-mini-transcribe"

    @classmethod
    def from_env(cls) -> "BatchSpeechConfig":
        return cls(
            api_key=os.getenv("OPENAI_API_KEY"),
            organization=os.getenv("OPENAI_ORG_ID") or os.getenv("OPENAI_ORGANIZATION"),
            project=os.getenv("OPENAI_PROJECT_ID") or os.getenv("OPENAI_PROJECT"),
            base_url=os.getenv("OPENAI_BASE_URL"),
            model=os.getenv("OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe"),
        )


def build_client(config: Optional[BatchSpeechConfig] = None) -> OpenAI:
    cfg = config or BatchSpeechConfig.from_env()
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.organization:
        kwargs["organization"] = cfg.organization
    if cfg.project:
        kwargs["project"] = cfg.project
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def transcribe_audio_file(file_path: str, config: Optional[BatchSpeechConfig] = None, **kwargs: Any) -> Any:
    client = build_client(config)
    cfg = config or BatchSpeechConfig.from_env()
    with open(file_path, "rb") as audio_file:
        return client.audio.transcriptions.create(model=cfg.model, file=audio_file, **kwargs)


def transcribe_audio_bytes(audio_bytes: bytes, filename: str = "audio.wav", config: Optional[BatchSpeechConfig] = None, **kwargs: Any) -> Any:
    client = build_client(config)
    cfg = config or BatchSpeechConfig.from_env()
    from io import BytesIO

    buffer = BytesIO(audio_bytes)
    buffer.name = filename
    return client.audio.transcriptions.create(model=cfg.model, file=buffer, **kwargs)
