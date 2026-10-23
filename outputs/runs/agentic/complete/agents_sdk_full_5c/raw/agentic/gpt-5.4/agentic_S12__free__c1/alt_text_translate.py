from __future__ import annotations

from typing import Optional

from deepl import DeepLClient


DEEPL_PROVIDER = "deepl"
DEEPL_API_HOST = "api-free.deepl.com"


def alt_text_translate(text: str, *, target_lang: str, source_lang: Optional[str] = None, glossary_id: Optional[str] = None) -> str:
    auth_key = __import__("os").getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    client = DeepLClient(auth_key)
    result = client.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang,
        glossary=glossary_id,
        preserve_formatting=True,
    )
    return result.text
