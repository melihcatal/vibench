from __future__ import annotations

from deepl import TextResult

from translation_client import build_translation_client, infer_source_lang, infer_target_lang
from translation_models import MarkupTranslationRequest, TranslationResponse, normalize_text


def translate_markup(markup: str, source_lang: str | None = None, target_lang: str | None = None) -> TranslationResponse:
    client = build_translation_client()
    req = MarkupTranslationRequest(
        markup=normalize_text(markup),
        source_lang=source_lang or infer_source_lang(),
        target_lang=target_lang or infer_target_lang(),
    )
    result: TextResult = client.translate_text(
        req.markup,
        source_lang=req.source_lang,
        target_lang=req.target_lang,
        tag_handling="html",
        preserve_formatting=True,
    )
    return TranslationResponse(
        translated_text=result.text,
        source_lang=req.source_lang,
        target_lang=req.target_lang,
        provider="deepl",
        raw=result,
    )
