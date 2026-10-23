import os
from functools import lru_cache
from typing import Any, Dict, Optional

from google.cloud import translate_v3 as translate


def _project_id() -> str:
    for name in ("GOOGLE_CLOUD_PROJECT", "GCLOUD_PROJECT", "GCP_PROJECT"):
        value = os.getenv(name)
        if value:
            return value
    raise RuntimeError("Google Cloud project environment variable is required")


@lru_cache(maxsize=1)
def get_translation_client() -> translate.TranslationServiceClient:
    return translate.TranslationServiceClient()


def parent_path(location: str = "global") -> str:
    return f"projects/{_project_id()}/locations/{location}"


def translate_text_request(text: str, source_language: str, target_language: str, mime_type: str = "text/plain") -> Dict[str, Any]:
    return {
        "parent": parent_path(),
        "contents": [text],
        "mime_type": mime_type,
        "source_language_code": source_language,
        "target_language_code": target_language,
    }


def translate_batch_request(texts, source_language: str, target_language: str, mime_type: str = "text/plain") -> Dict[str, Any]:
    return {
        "parent": parent_path(),
        "contents": list(texts),
        "mime_type": mime_type,
        "source_language_code": source_language,
        "target_language_code": target_language,
    }
