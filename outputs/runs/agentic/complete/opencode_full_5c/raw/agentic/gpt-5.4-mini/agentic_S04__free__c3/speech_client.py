import os
from typing import Any, Dict, Optional

import openai


def get_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return key


def get_client() -> openai.OpenAI:
    return openai.OpenAI(api_key=get_api_key())


def get_model() -> str:
    return os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-transcribe")


def build_transcription_config(
    overrides: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    config: Dict[str, Any] = {"model": get_model()}
    if overrides:
        config.update(overrides)
    return config
