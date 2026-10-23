from dataclasses import dataclass
import os
from typing import Optional

from mistralai import Mistral


@dataclass
class LLMConfig:
    model: str
    temperature: float = 0.2
    max_tokens: int = 1024


def get_api_key() -> str:
    key = os.getenv("MISTRAL_API_KEY")
    if not key:
        raise RuntimeError("MISTRAL_API_KEY is required")
    return key


def get_client() -> Mistral:
    return Mistral(api_key=get_api_key())


def choose_model(task: str) -> str:
    task = task.lower()
    if "summar" in task:
        return os.getenv("MISTRAL_SUMMARY_MODEL", "mistral-large-latest")
    if "json" in task or "extract" in task:
        return os.getenv("MISTRAL_EXTRACTION_MODEL", "mistral-large-latest")
    if "answer" in task:
        return os.getenv("MISTRAL_QA_MODEL", "mistral-medium-latest")
    if "stream" in task:
        return os.getenv("MISTRAL_STREAM_MODEL", "mistral-large-latest")
    return os.getenv("MISTRAL_DEFAULT_MODEL", "mistral-large-latest")
