import os
from typing import Any, Dict

from security_models import normalize_mapping, normalize_text


def load_security_config() -> Dict[str, Any]:
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "openai_model": os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        "azure_key_vault_url": os.getenv("AZURE_KEY_VAULT_URL", ""),
        "azure_key_vault_key_name": os.getenv("AZURE_KEY_VAULT_KEY_NAME", ""),
    }


def build_openai_headers() -> Dict[str, str]:
    key = normalize_text(os.getenv("OPENAI_API_KEY", ""))
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"} if key else {}


def build_openai_payload(prompt: str) -> Dict[str, Any]:
    return {
        "model": normalize_text(os.getenv("OPENAI_MODEL", "gpt-5.4-mini")),
        "input": normalize_text(prompt),
    }


def merge_context(base: Dict[str, Any], extra: Dict[str, Any]) -> Dict[str, Any]:
    merged = normalize_mapping(base)
    merged.update(normalize_mapping(extra))
    return merged
