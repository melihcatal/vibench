import os
from typing import Optional, AsyncIterator

import deepl

from speech_models import StreamingRecognitionResult, normalize_transcript_text


DEEPL_API_HOST = "api.deepl.com"


def load_deepl_auth_key() -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError(
            "DEEPL_AUTH_KEY environment variable is required for DeepL API"
        )
    return auth_key


def create_deepl_translator(
    auth_key: Optional[str] = None,
    server_url: Optional[str] = None,
) -> deepl.Translator:
    key = auth_key or load_deepl_auth_key()
    kwargs = {"auth_key": key}
    if server_url:
        kwargs["server_url"] = server_url
    return deepl.Translator(**kwargs)


class CaptionTranslationResult:
    def __init__(
        self,
        source_text: str,
        translated_text: str,
        source_lang: str,
        target_lang: str,
        confidence: float = 1.0,
    ):
        self.source_text = source_text
        self.translated_text = translated_text
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.confidence = confidence


async def translate_caption(
    text: str,
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
    formality: Optional[str] = None,
    preserve_formatting: bool = True,
) -> CaptionTranslationResult:
    if translator is None:
        translator = create_deepl_translator()

    translate_kwargs = {
        "target_lang": target_lang,
        "preserve_formatting": preserve_formatting,
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang
    if formality:
        translate_kwargs["formality"] = formality

    result = translator.translate_text(text, **translate_kwargs)

    detected_source = (
        result.detected_source_lang
        if result.detected_source_lang
        else source_lang or "EN"
    )

    return CaptionTranslationResult(
        source_text=text,
        translated_text=result.text,
        source_lang=detected_source,
        target_lang=target_lang,
        confidence=1.0,
    )


async def translate_live_captions(
    caption_stream: AsyncIterator[StreamingRecognitionResult],
    target_lang: str = "ES",
    translator: Optional[deepl.Translator] = None,
    formality: Optional[str] = None,
) -> AsyncIterator[CaptionTranslationResult]:
    if translator is None:
        translator = create_deepl_translator()

    async for caption in caption_stream:
        if caption.is_final and caption.text.strip():
            normalized = normalize_transcript_text(caption)
            translation = await translate_caption(
                text=normalized,
                target_lang=target_lang,
                translator=translator,
                formality=formality,
            )
            yield translation


async def translate_caption_batch(
    texts: list[str],
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
) -> list[CaptionTranslationResult]:
    if translator is None:
        translator = create_deepl_translator()

    translate_kwargs = {"target_lang": target_lang}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    results = translator.translate_text(texts, **translate_kwargs)

    translations = []
    for i, result in enumerate(results):
        detected = (
            result.detected_source_lang
            if result.detected_source_lang
            else source_lang or "EN"
        )
        translations.append(
            CaptionTranslationResult(
                source_text=texts[i],
                translated_text=result.text,
                source_lang=detected,
                target_lang=target_lang,
            )
        )
    return translations
