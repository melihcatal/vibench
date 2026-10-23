from __future__ import annotations

import os
import logging
from collections.abc import AsyncGenerator

import deepl

from speech_models import TranscriptResult, StreamingEvent

logger = logging.getLogger(__name__)


def create_deepl_translator(api_key: str | None = None) -> deepl.Translator:
    key = api_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")
    return deepl.Translator(key)


async def translate_live_captions(
    source: AsyncGenerator[StreamingEvent, None],
    target_language: str = "ES",
    source_language: str | None = None,
    translator: deepl.Translator | None = None,
) -> AsyncGenerator[StreamingEvent, None]:
    if translator is None:
        translator = create_deepl_translator()

    async for event in source:
        if event.result is None or not event.result.text.strip():
            yield event
            continue

        try:
            translate_options = {}
            if source_language:
                translate_options["source_lang"] = source_language

            result = translator.translate_text(
                event.result.text,
                target_lang=target_language,
                **translate_options,
            )

            translated_result = TranscriptResult(
                is_final=event.result.is_final,
                text=result.text,
                segments=event.result.segments,
                language=target_language.lower(),
                channel_index=event.result.channel_index,
                timestamp=event.result.timestamp,
            )

            yield StreamingEvent(
                event_type=event.event_type,
                result=translated_result,
                raw_payload=event.raw_payload,
            )
        except Exception as exc:
            logger.error("DeepL translation error: %s", exc)
            yield event
