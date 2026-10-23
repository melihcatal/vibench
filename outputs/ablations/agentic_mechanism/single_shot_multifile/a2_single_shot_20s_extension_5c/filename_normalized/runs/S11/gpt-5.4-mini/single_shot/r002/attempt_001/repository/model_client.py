import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI

from model_models import GenerationInput, ResourceSelection, normalize_generation_input, normalize_resource_selection

DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model_name(model: Optional[str] = None) -> str:
    return model or DEFAULT_OPENAI_MODEL


def resolve_generation_input(request: Dict[str, Any] | GenerationInput) -> GenerationInput:
    return normalize_generation_input(request)


def resolve_resource_selection(request: Dict[str, Any] | ResourceSelection) -> ResourceSelection:
    return normalize_resource_selection(request)
