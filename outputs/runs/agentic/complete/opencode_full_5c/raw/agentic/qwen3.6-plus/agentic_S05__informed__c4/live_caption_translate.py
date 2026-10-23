import os
from typing import Optional

import deepl

from speech_models import NormalizedTranscript


def load_deepl_config(auth_key: Optional[str] = None) -> dict:
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    return {"auth_key": key}


def create_deepl_translator(auth_key: Optional[str] = None) -> deepl.Translator:
    config = load_deepl_config(auth_key)
    return deepl.Translator(config["auth_key"])


async def translate_caption(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
) -> str:
    if translator is None:
        translator = create_deepl_translator(auth_key)

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: translator.translate_text(
            text,
            source_lang=source_lang,
            target_lang=target_lang,
        ),
    )
    return result.text


async def translate_captions_batch(
    captions: list[NormalizedTranscript],
    target_lang: str,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
) -> list[NormalizedTranscript]:
    if translator is None:
        translator = create_deepl_translator(auth_key)

    translated = []
    for caption in captions:
        text = await translate_caption(
            caption.text,
            target_lang=target_lang,
            source_lang=source_lang or caption.language,
            auth_key=auth_key,
            translator=translator,
        )
        translated_caption = NormalizedTranscript(
            text=text,
            confidence=caption.confidence,
            start_time=caption.start_time,
            end_time=caption.end_time,
            is_final=caption.is_final,
            words=caption.words,
            speaker=caption.speaker,
            language=target_lang.lower()[:2],
        )
        translated.append(translated_caption)

    return translated


async def translate_live_caption_stream(
    caption_stream,
    target_lang: str,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
    translator: Optional[deepl.Translator] = None,
):
    if translator is None:
        translator = create_deepl_translator(auth_key)

    async for caption in caption_stream:
        translated_text = await translate_caption(
            caption.text,
            target_lang=target_lang,
            source_lang=source_lang or caption.language,
            auth_key=auth_key,
            translator=translator,
        )
        yield NormalizedTranscript(
            text=translated_text,
            confidence=caption.confidence,
            start_time=caption.start_time,
            end_time=caption.end_time,
            is_final=caption.is_final,
            words=caption.words,
            speaker=caption.speaker,
            language=target_lang.lower()[:2],
        )


import asyncio
