"""
Starts a streaming recognizer with language and punctuation settings using Deepgram Streaming API.

Configures and starts a Deepgram streaming speech-to-text session with
explicit language detection, multiple language support, punctuation options,
and formatting preferences.

Requires:
    pip install deepgram-sdk
"""

import asyncio
from typing import AsyncIterator, Optional, List

from deepgram import DeepgramClient, LiveOptions

from speech_client import build_deepgram_client, validate_audio_params
from speech_models import (
    SpeechConfig,
    TranscriptChunk,
    TranscriptStatus,
)


LANGUAGE_MAP = {
    "en": "en",
    "en-US": "en-US",
    "en-GB": "en-GB",
    "es": "es",
    "es-ES": "es-ES",
    "es-MX": "es-MX",
    "fr": "fr",
    "fr-FR": "fr-FR",
    "de": "de",
    "de-DE": "de-DE",
    "ja": "ja",
    "ja-JP": "ja-JP",
    "zh": "zh",
    "zh-CN": "zh-CN",
    "ko": "ko",
    "ko-KR": "ko-KR",
    "pt": "pt",
    "pt-BR": "pt-BR",
    "it": "it",
    "it-IT": "it-IT",
    "ru": "ru",
    "ru-RU": "ru-RU",
    "ar": "ar",
    "hi": "hi",
    "hi-IN": "hi-IN",
}


def resolve_language_code(language: str) -> str:
    """Resolve a language identifier to a Deepgram-compatible code.

    Args:
        language: Language code or locale string.

    Returns:
        Resolved Deepgram language code.
    """
    return LANGUAGE_MAP.get(language, language)


async def start_streaming_recognizer(
    audio_source,
    language: str = "en",
    model: str = "nova-2",
    sample_rate: int = 16000,
    channels: int = 1,
    punctuate: bool = True,
    smart_format: bool = True,
    interim_results: bool = True,
    profanity_filter: bool = False,
    diarize: bool = False,
    keywords: Optional[List[str]] = None,
    encoding: str = "linear16",
    api_key: Optional[str] = None,
) -> AsyncIterator[TranscriptChunk]:
    """Start a Deepgram streaming recognizer with language and punctuation settings.

    Establishes a streaming connection to Deepgram's Speech-to-Text API with
    configurable language, punctuation, and formatting options.

    Args:
        audio_source: Async iterable yielding audio bytes.
        language: Language code (e.g., 'en', 'es', 'ja', 'en-US').
        model: Deepgram model identifier (e.g., 'nova-2', 'nova-2-general').
        sample_rate: Audio sample rate in Hz.
        channels: Number of audio channels.
        punctuate: Whether to add punctuation to transcripts.
        smart_format: Enable Deepgram smart formatting.
        interim_results: Whether to return interim results.
        profanity_filter: Filter profanity from transcripts.
        diarize: Enable speaker diarization.
        keywords: List of keywords to boost recognition for.
        encoding: Audio encoding format.
        api_key: Deepgram API key.

    Yields:
        TranscriptChunk objects with transcribed text.
    """
    validate_audio_params(sample_rate=sample_rate, channels=channels, encoding=encoding)

    resolved_lang = resolve_language_code(language)

    client = build_deepgram_client(api_key=api_key)

    live_options = LiveOptions(
        model=model,
        language=resolved_lang,
        sample_rate=sample_rate,
        channels=channels,
        encoding=encoding,
        smart_format=smart_format,
        interim_results=interim_results,
        punctuate=punctuate,
        profanity_filter=profanity_filter,
        diarize=diarize,
    )

    if keywords:
        live_options.keywords = keywords

    async with client.listen.live.v("1") as connection:
        send_task = asyncio.create_task(
            _stream_audio(connection, audio_source)
        )

        async for result in connection.results:
            transcript_text = ""
            confidence = 0.0

            if hasattr(result, "channel") and result.channel:
                alternatives = getattr(result.channel, "alternatives", [])
                if alternatives:
                    transcript_text = alternatives[0].transcript
                    confidence = alternatives[0].confidence

            is_final = getattr(result, "is_final", False)

            if transcript_text.strip():
                chunk = TranscriptChunk(
                    text=transcript_text,
                    status=TranscriptStatus.FINAL if is_final else TranscriptStatus.INTERIM,
                    confidence=confidence,
                    is_final=is_final,
                )
                yield chunk

        send_task.cancel()
        try:
            await send_task
        except asyncio.CancelledError:
            pass


async def start_streaming_with_config(
    audio_source,
    config: SpeechConfig,
    api_key: Optional[str] = None,
) -> AsyncIterator[TranscriptChunk]:
    """Start a streaming recognizer using a SpeechConfig object.

    Args:
        audio_source: Async iterable yielding audio bytes.
        config: SpeechConfig with all recognition settings.
        api_key: Deepgram API key.

    Yields:
        TranscriptChunk objects from the streaming recognizer.
    """
    async for chunk in start_streaming_recognizer(
        audio_source=audio_source,
        language=config.language,
        model=config.model,
        sample_rate=config.sample_rate,
        channels=config.channels,
        punctuate=config.punctuate,
        smart_format=config.smart_format,
        interim_results=config.interim_results,
        profanity_filter=config.profanity_filter,
        diarize=config.diarize,
        keywords=config.keywords,
        encoding=config.encoding,
        api_key=api_key,
    ):
        yield chunk


async def _stream_audio(connection, audio_source) -> None:
    """Stream audio chunks to Deepgram connection."""
    try:
        async for chunk in audio_source:
            data = chunk.data if hasattr(chunk, "data") else chunk
            await connection.send(data)
    except Exception:
        pass
    finally:
        await connection.finish()


if __name__ == "__main__":
    async def main():
        async def dummy_audio():
            for _ in range(10):
                yield b"\x00" * 4096

        async for chunk in start_streaming_recognizer(
            audio_source=dummy_audio(),
            language="en",
            punctuate=True,
        ):
            print(f"[{'FINAL' if chunk.is_final else 'INTERIM'}] {chunk.text}")

    asyncio.run(main())
