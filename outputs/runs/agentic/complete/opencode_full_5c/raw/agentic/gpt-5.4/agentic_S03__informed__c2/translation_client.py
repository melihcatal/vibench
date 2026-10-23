from __future__ import annotations

import os
from typing import Iterable, List, Optional

import deepl

from translation_models import normalize_language_code


DEEPL_PROVIDER = "DeepL API"
DEEPL_MODEL = "general"


def get_deepl_client() -> deepl.Translator:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    server_url = os.getenv("DEEPL_SERVER_URL")
    if server_url:
        return deepl.Translator(auth_key, server_url=server_url)
    return deepl.Translator(auth_key)


def deepl_language_code(language: Optional[str]) -> Optional[str]:
    code = normalize_language_code(language)
    if code is None:
        return None
    return code.upper()


def translate_text_with_deepl(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    *,
    tag_handling: Optional[str] = None,
) -> deepl.TextResult:
    client = get_deepl_client()
    options = {
        "target_lang": deepl_language_code(target_language),
        "source_lang": deepl_language_code(source_language),
    }
    if tag_handling:
        options["tag_handling"] = tag_handling
    return client.translate_text(text, **options)


def translate_texts_with_deepl(
    texts: Iterable[str],
    target_language: str,
    source_language: Optional[str] = None,
) -> List[deepl.TextResult]:
    client = get_deepl_client()
    return client.translate_text(
        list(texts),
        target_lang=deepl_language_code(target_language),
        source_lang=deepl_language_code(source_language),
    )
