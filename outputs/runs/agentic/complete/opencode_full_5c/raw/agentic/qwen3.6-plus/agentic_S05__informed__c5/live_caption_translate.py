import os
from typing import Optional

import deepl

from speech_models import FinalTranscript


def load_deepl_config() -> dict:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    return {"auth_key": auth_key}


def create_deepl_translator(auth_key: Optional[str] = None) -> deepl.Translator:
    if auth_key is None:
        config = load_deepl_config()
        auth_key = config["auth_key"]
    return deepl.Translator(auth_key)


async def translate_caption(
    transcript: FinalTranscript,
    target_language: str = "ES",
    translator: Optional[deepl.Translator] = None,
) -> str:
    if translator is None:
        translator = create_deepl_translator()

    text = transcript.text
    if not text:
        return ""

    result = translator.translate_text(
        text,
        target_lang=target_language,
        source_lang=transcript.language.upper() if transcript.language else None,
    )
    return result.text


async def translate_captions_stream(
    transcript_stream,
    target_language: str = "ES",
    translator: Optional[deepl.Translator] = None,
):
    if translator is None:
        translator = create_deepl_translator()

    async for transcript in transcript_stream:
        if isinstance(transcript, FinalTranscript) and transcript.text:
            translated_text = await translate_caption(
                transcript, target_language, translator
            )
            yield translated_text
        elif hasattr(transcript, "final") and transcript.final:
            translated_text = await translate_caption(
                transcript.final, target_language, translator
            )
            yield translated_text
