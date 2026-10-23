import os
from typing import Any, Dict

from google.cloud import translate_v2 as translate


def get_google_project_id() -> str:
    return os.environ.get("GOOGLE_CLOUD_PROJECT", "")


def get_translation_client() -> translate.Client:
    return translate.Client()


def translate_text_google(text: str, source_language: str, target_language: str) -> Dict[str, Any]:
    client = get_translation_client()
    result = client.translate(text, source_language=source_language, target_language=target_language, format_="text")
    return result


def translate_html_google(html: str, source_language: str, target_language: str) -> Dict[str, Any]:
    client = get_translation_client()
    result = client.translate(html, source_language=source_language, target_language=target_language, format_="html")
    return result


def translate_batch_google(texts, source_language: str, target_language: str):
    client = get_translation_client()
    return client.translate(texts, source_language=source_language, target_language=target_language, format_="text")
