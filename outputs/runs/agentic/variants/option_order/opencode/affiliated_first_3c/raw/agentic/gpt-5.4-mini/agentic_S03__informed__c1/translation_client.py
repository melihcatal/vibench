import os
from typing import Any, Dict

from deepl import Translator


def get_deepl_auth_key() -> str:
    return os.environ.get("DEEPL_AUTH_KEY", "")


def build_translation_client() -> Translator:
    auth_key = get_deepl_auth_key()
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    return Translator(auth_key)


def detect_target_formality(options: Dict[str, Any]) -> Any:
    return options.get("formality")


def extract_translated_text(result: Any) -> str:
    if hasattr(result, "text"):
        return result.text
    return str(result)
