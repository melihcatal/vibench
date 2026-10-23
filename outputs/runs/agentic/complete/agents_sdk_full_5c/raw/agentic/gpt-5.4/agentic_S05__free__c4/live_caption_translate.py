from __future__ import annotations

from typing import Iterable

from deepl import Translator

from speech_models import CaptionChunk, TranslationResult, merge_caption_chunks


def translate_live_captions(
    chunks: Iterable[CaptionChunk],
    target_language: str,
    auth_key: str,
) -> TranslationResult:
    translator = Translator(auth_key)
    text = merge_caption_chunks(chunks)
    result = translator.translate_text(text, target_lang=target_language)
    return TranslationResult(
        translated_text=result.text,
        target_language=target_language,
        raw={"detected_source_lang": getattr(result, "detected_source_lang", None), "provider": "DeepL"},
    )
