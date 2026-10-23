"""
Translate live captions into another language using DeepL API.

Translates streaming caption/transcript text into a target language using
the DeepL translation API, supporting real-time translation of live captions.

Requires:
    pip install deepl
"""

import os
from typing import Optional, Iterator

import deepl

from speech_models import TranscriptChunk, TranscriptStatus


def get_deepl_client(auth_key: Optional[str] = None) -> deepl.Translator:
    """Create a DeepL translator client.

    Args:
        auth_key: DeepL authentication key. Falls back to DEEPL_AUTH_KEY env var.

    Returns:
        Configured DeepL Translator instance.

    Raises:
        ValueError: If no auth key is provided or found in environment.
    """
    key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError(
            "DEEPL_AUTH_KEY environment variable is required, "
            "or pass auth_key parameter"
        )
    return deepl.Translator(key)


def translate_caption(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
    formality: Optional[str] = None,
) -> str:
    """Translate a single caption text using DeepL API.

    Args:
        text: Caption text to translate.
        target_lang: Target language code (e.g., 'ES', 'FR', 'JA', 'ZH').
        source_lang: Source language code (e.g., 'EN'). Auto-detected if None.
        auth_key: DeepL auth key. Falls back to DEEPL_AUTH_KEY env var.
        formality: Formality level ('more' or 'less') for supported languages.

    Returns:
        Translated text string.
    """
    if not text.strip():
        return text

    client = get_deepl_client(auth_key=auth_key)

    translate_kwargs = {
        "target_lang": target_lang.upper(),
    }

    if source_lang:
        translate_kwargs["source_lang"] = source_lang.upper()

    if formality:
        translate_kwargs["formality"] = formality

    result = client.translate_text(text, **translate_kwargs)
    return result.text


def translate_caption_chunk(
    chunk: TranscriptChunk,
    target_lang: str,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> TranscriptChunk:
    """Translate a transcript chunk into another language.

    Args:
        chunk: Original TranscriptChunk to translate.
        target_lang: Target language code (e.g., 'ES', 'FR', 'DE').
        source_lang: Source language code. Auto-detected if None.
        auth_key: DeepL auth key.

    Returns:
        New TranscriptChunk with translated text.
    """
    translated_text = translate_caption(
        text=chunk.text,
        target_lang=target_lang,
        source_lang=source_lang,
        auth_key=auth_key,
    )

    return TranscriptChunk(
        text=translated_text,
        status=chunk.status,
        confidence=chunk.confidence,
        start_time=chunk.start_time,
        end_time=chunk.end_time,
        speaker=chunk.speaker,
        is_final=chunk.is_final,
        timestamp=chunk.timestamp,
    )


def translate_live_captions(
    caption_stream: Iterator[TranscriptChunk],
    target_lang: str,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> Iterator[TranscriptChunk]:
    """Translate a stream of live captions using DeepL API.

    Consumes an iterator of TranscriptChunk objects, translates each chunk
    into the target language via DeepL, and yields translated chunks.

    Args:
        caption_stream: Iterator of TranscriptChunk objects to translate.
        target_lang: Target language code (e.g., 'ES', 'FR', 'JA', 'ZH').
        source_lang: Source language code. Auto-detected if None.
        auth_key: DeepL auth key. Falls back to DEEPL_AUTH_KEY env var.

    Yields:
        Translated TranscriptChunk objects.
    """
    client = get_deepl_client(auth_key=auth_key)

    translate_kwargs = {
        "target_lang": target_lang.upper(),
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang.upper()

    for chunk in caption_stream:
        if not chunk.text.strip():
            yield chunk
            continue

        result = client.translate_text(chunk.text, **translate_kwargs)
        translated_text = result.text

        yield TranscriptChunk(
            text=translated_text,
            status=chunk.status,
            confidence=chunk.confidence,
            start_time=chunk.start_time,
            end_time=chunk.end_time,
            speaker=chunk.speaker,
            is_final=chunk.is_final,
            timestamp=chunk.timestamp,
        )


async def translate_live_captions_async(
    caption_stream,
    target_lang: str,
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
):
    """Async generator to translate live captions using DeepL API.

    Args:
        caption_stream: Async iterator of TranscriptChunk objects.
        target_lang: Target language code (e.g., 'ES', 'FR', 'DE').
        source_lang: Source language code. Auto-detected if None.
        auth_key: DeepL auth key.

    Yields:
        Translated TranscriptChunk objects.
    """
    client = get_deepl_client(auth_key=auth_key)

    translate_kwargs = {
        "target_lang": target_lang.upper(),
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang.upper()

    async for chunk in caption_stream:
        if not chunk.text.strip():
            yield chunk
            continue

        result = client.translate_text(chunk.text, **translate_kwargs)

        yield TranscriptChunk(
            text=result.text,
            status=chunk.status,
            confidence=chunk.confidence,
            start_time=chunk.start_time,
            end_time=chunk.end_time,
            speaker=chunk.speaker,
            is_final=chunk.is_final,
            timestamp=chunk.timestamp,
        )


if __name__ == "__main__":
    chunks = [
        TranscriptChunk(text="Hello, how are you today?", status=TranscriptStatus.FINAL, is_final=True),
        TranscriptChunk(text="I hope you are doing well.", status=TranscriptStatus.FINAL, is_final=True),
    ]

    for translated in translate_live_captions(iter(chunks), target_lang="ES"):
        print(f"[{translated.status.value}] {translated.text}")
