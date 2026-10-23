import os
from typing import Optional

from openai import OpenAI

from security_models import SecretRequest, normalize_secret_name, normalize_stage


def load_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def secret_identifier(request: SecretRequest) -> str:
    name = normalize_secret_name(request.name)
    stage = normalize_stage(request.stage)
    version = str(request.version).strip() if request.version is not None else None
    if version:
        return f"{name}:{version}"
    if stage:
        return f"{name}:{stage}"
    return name


def provider_model() -> str:
    return os.environ.get("OPENAI_MODEL", "gpt-5.4-mini")


def system_prompt() -> str:
    return "Return the requested secret data as structured JSON only."
