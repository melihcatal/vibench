import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class SpeechConfig:
    openai_api_key: str
    openai_base_url: str
    openai_transcription_model: str
    openai_translation_model: str
    openai_moderation_model: str
    openai_embeddings_model: str


def load_config() -> SpeechConfig:
    return SpeechConfig(
        openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
        openai_base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        openai_transcription_model=os.environ.get("OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-transcribe"),
        openai_translation_model=os.environ.get("OPENAI_TRANSLATION_MODEL", "gpt-4o-mini"),
        openai_moderation_model=os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest"),
        openai_embeddings_model=os.environ.get("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small"),
    )


def openai_headers(config: SpeechConfig) -> Dict[str, str]:
    return {"Authorization": f"Bearer {config.openai_api_key}"}


def openai_post(config: SpeechConfig, path: str, *, data: Optional[Dict[str, Any]] = None, files: Any = None, json: Any = None) -> requests.Response:
    return requests.post(f"{config.openai_base_url.rstrip('/')}/{path.lstrip('/')}", headers=openai_headers(config), data=data, files=files, json=json, timeout=120)


def openai_get(config: SpeechConfig, path: str) -> requests.Response:
    return requests.get(f"{config.openai_base_url.rstrip('/')}/{path.lstrip('/')}", headers=openai_headers(config), timeout=120)
