from __future__ import annotations

from typing import Iterable, Optional

from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResult, normalize_text


def translate_markup(
    markup: str,
    target_language: str,
    source_language: Optional[str] = None,
    ignore_tags: Optional[Iterable[str]] = None,
) -> TranslationResult:
    client = get_translation_client()
    request = TranslationRequest(
        text=normalize_text(markup),
        source_language=source_language,
        target_language=target_language,
        preserve_formatting=True,
    )
    return client.translate_text(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
        tag_handling="html",
        split_sentences="nonewlines",
        preserve_formatting=True,
        outline_detection=False,
        ignore_tags=ignore_tags,
    )
