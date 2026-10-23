"""
Start a Google Cloud Speech-to-Text streaming recognizer with language and punctuation settings.

Configures and launches a streaming recognition session with explicit language code
and automatic punctuation options.

Provider: Google Cloud Speech-to-Text
SDK: google-cloud-speech
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

from __future__ import annotations

import time
from typing import AsyncGenerator, Optional

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types as speech_types

from speech_client import create_streaming_speech_client, build_streaming_config
from speech_models import extract_interim_transcript, extract_final_transcripts


async def start_streaming_recognizer_with_language(
    audio_stream: AsyncGenerator[bytes, None],
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    enable_punctuation: bool = True,
    encoding: speech_types.RecognitionConfig.AudioEncoding = speech_types.RecognitionConfig.AudioEncoding.LINEAR16,
    model: str = "default",
    use_enhanced: bool = False,
    max_alternatives: int = 1,
    alternative_language_codes: Optional[list[str]] = None,
) -> AsyncGenerator[dict, None]:
    """
    Start a Google Cloud Speech streaming recognizer with language and punctuation settings.

    Configures the streaming recognition session with the specified language code,
    automatic punctuation, and other recognition parameters, then processes audio
    from the provided async generator and yields transcription results.

    Args:
        audio_stream: Async generator yielding raw audio bytes.
        language_code: Primary BCP-47 language code (e.g., 'en-US', 'es-ES', 'fr-FR').
        sample_rate_hertz: Audio sample rate in Hz.
        enable_punctuation: Whether to enable automatic punctuation.
        encoding: Audio encoding format.
        model: Speech model to use (e.g., 'default', 'phone_call', 'video').
        use_enhanced: Whether to use enhanced recognition models.
        max_alternatives: Maximum number of alternative transcriptions.
        alternative_language_codes: Optional additional language codes for multi-language.

    Yields:
        Dict with keys:
            - 'type': 'interim' or 'final'
            - 'text': Transcribed text
            - 'confidence': Confidence score
            - 'language_code': Detected/used language code
            - 'timestamp': Event timestamp
    """
    recognition_config = speech_types.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
        max_alternatives=max_alternatives,
        model=model,
        use_enhanced=use_enhanced,
    )

    if alternative_language_codes:
        recognition_config.alternative_language_codes = alternative_language_codes

    streaming_config = speech_types.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
    )

    client = create_streaming_speech_client()

    try:
        responses = client.streaming_recognize(
            config=_request_generator(streaming_config, audio_stream)
        )

        for response in responses:
            interim_text = extract_interim_transcript(response)
            if interim_text:
                yield {
                    "type": "interim",
                    "text": interim_text,
                    "confidence": 0.0,
                    "language_code": language_code,
                    "timestamp": time.time(),
                }

            final_texts = extract_final_transcripts(response)
            for final_text in final_texts:
                for result in response.results:
                    if result.is_final and result.alternatives:
                        yield {
                            "type": "final",
                            "text": final_text,
                            "confidence": result.alternatives[0].confidence,
                            "language_code": language_code,
                            "timestamp": time.time(),
                        }
                        break

    except Exception as e:
        yield {
            "type": "error",
            "text": "",
            "confidence": 0.0,
            "language_code": language_code,
            "timestamp": time.time(),
            "error": str(e),
        }


def _request_generator(
    streaming_config: speech_types.StreamingRecognitionConfig,
    audio_stream: AsyncGenerator[bytes, None],
):
    """
    Synchronous generator that wraps an async audio stream for the Google Cloud Speech API.

    The streaming_recognize method expects a sync generator. This function
    bridges async audio production with the sync API expectation using
    synchronous iteration over the pre-collected audio.

    Args:
        streaming_config: Pre-built streaming recognition config.
        audio_stream: Async generator of audio bytes.

    Yields:
        StreamingRecognizeRequest objects.
    """
    import asyncio

    yield speech_types.StreamingRecognizeRequest(streaming_config=streaming_config)

    async def _collect_audio():
        """Collect all audio from the async stream."""
        chunks = []
        async for chunk in audio_stream:
            chunks.append(chunk)
        return chunks

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        all_chunks = loop.run_until_complete(_collect_audio())
    finally:
        loop.close()

    for chunk in all_chunks:
        yield speech_types.StreamingRecognizeRequest(audio_content=chunk)
