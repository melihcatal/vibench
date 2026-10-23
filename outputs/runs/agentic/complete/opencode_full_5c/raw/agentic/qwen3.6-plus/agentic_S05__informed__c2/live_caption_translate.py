import os
from typing import List, Optional

import deepl

from speech_models import TranscriptResult


def get_deepl_auth_key() -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")
    return auth_key


def create_deepl_translator(auth_key: Optional[str] = None) -> deepl.Translator:
    key = auth_key or get_deepl_auth_key()
    return deepl.Translator(key)


def translate_caption(
    translator: deepl.Translator,
    text: str,
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
    preserve_formatting: bool = True,
) -> str:
    if not text.strip():
        return ""

    options = {
        "preserve_formatting": preserve_formatting,
    }
    if source_lang:
        options["source_lang"] = source_lang

    result = translator.translate_text(text, target_lang=target_lang, **options)
    return result.text


def translate_transcript_result(
    translator: deepl.Translator,
    result: TranscriptResult,
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
) -> TranscriptResult:
    translated_text = translate_caption(
        translator,
        result.text,
        target_lang=target_lang,
        source_lang=source_lang,
    )

    return TranscriptResult(
        text=translated_text,
        transcript_type=result.transcript_type,
        confidence=result.confidence,
        words=result.words,
        language=target_lang.lower(),
        channel=result.channel,
        timestamp=result.timestamp,
        result_id=result.result_id,
        is_final=result.is_final,
        speech_final=result.speech_final,
        duration=result.duration,
        start_time=result.start_time,
    )


def translate_captions_batch(
    translator: deepl.Translator,
    texts: List[str],
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
) -> List[str]:
    if not texts:
        return []

    options = {}
    if source_lang:
        options["source_lang"] = source_lang

    results = translator.translate_text(texts, target_lang=target_lang, **options)
    return [r.text for r in results]


class LiveCaptionTranslator:
    def __init__(
        self,
        target_lang: str = "ES",
        source_lang: Optional[str] = None,
        auth_key: Optional[str] = None,
    ):
        self.target_lang = target_lang
        self.source_lang = source_lang
        self._translator = create_deepl_translator(auth_key)
        self._translation_cache: dict = {}

    def translate(self, text: str) -> str:
        if text in self._translation_cache:
            return self._translation_cache[text]

        translated = translate_caption(
            self._translator,
            text,
            target_lang=self.target_lang,
            source_lang=self.source_lang,
        )
        self._translation_cache[text] = translated
        return translated

    def translate_result(self, result: TranscriptResult) -> TranscriptResult:
        return translate_transcript_result(
            self._translator,
            result,
            target_lang=self.target_lang,
            source_lang=self.source_lang,
        )

    def translate_batch(self, texts: List[str]) -> List[str]:
        return translate_captions_batch(
            self._translator,
            texts,
            target_lang=self.target_lang,
            source_lang=self.source_lang,
        )

    def clear_cache(self):
        self._translation_cache.clear()
