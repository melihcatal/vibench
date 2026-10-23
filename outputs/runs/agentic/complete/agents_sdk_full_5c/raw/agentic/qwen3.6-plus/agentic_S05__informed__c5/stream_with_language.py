"""Starts a streaming recognizer with language and punctuation settings via Google Cloud Speech-to-Text."""

from typing import AsyncIterator, AsyncGenerator, Optional
from google.cloud.speech_v2.types import cloud_speech
from speech_client import get_speech_client, build_recognizer_path
from speech_models import StreamingSpeechResult, normalize_recognition_result


def build_streaming_config(
    language_codes: list[str],
    model: str = "latest_long",
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    max_alternatives: int = 1,
) -> cloud_speech.StreamingRecognitionConfig:
    """
    Build a StreamingRecognitionConfig for Google Cloud Speech-to-Text v2
    with explicit language codes and punctuation settings.
    """
    return cloud_speech.StreamingRecognitionConfig(
        config=cloud_speech.RecognitionConfig(
            language_codes=language_codes,
            model=model,
            automatic_punctuation=enable_automatic_punctuation,
            enable_word_time_offsets=enable_word_time_offsets,
            max_alternative_count=max_alternatives,
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        ),
    )


async def stream_with_language(
    audio_chunks: AsyncIterator[bytes],
    project_id: str,
    language_codes: list[str] | None = None,
    enable_punctuation: bool = True,
    model: str = "latest_long",
) -> AsyncGenerator[StreamingSpeechResult, None]:
    """
    Start a streaming recognizer with language and punctuation settings using
    Google Cloud Speech-to-Text v2 streaming API.

    Uses google-cloud-speech SDK with speech.googleapis.com endpoint.
    Model: latest_long or latest_short via google-cloud-speech.
    """
    codes = language_codes or ["en-US"]
    recognizer = build_recognizer_path(project_id=project_id)
    client = get_speech_client()

    streaming_config = build_streaming_config(
        language_codes=codes,
        model=model,
        enable_automatic_punctuation=enable_punctuation,
    )

    async def request_generator():
        yield cloud_speech.StreamingRecognizeRequest(
            recognizer=recognizer,
            streaming_config=streaming_config,
        )
        async for chunk in audio_chunks:
            if chunk:
                yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    responses = client.streaming_recognize(requests=request_generator())

    for response in responses:
        for result in response.results:
            normalized = normalize_recognition_result(result)
            yield normalized


async def stream_with_multilingual(
    audio_chunks: AsyncIterator[bytes],
    project_id: str,
    primary_language: str = "en-US",
    secondary_languages: list[str] | None = None,
    enable_punctuation: bool = True,
) -> AsyncGenerator[StreamingSpeechResult, None]:
    """
    Start a multilingual streaming recognizer via Google Cloud Speech-to-Text.

    Configures multiple language codes for automatic language detection.
    Uses google-cloud-speech SDK with speech.googleapis.com.
    """
    all_languages = [primary_language]
    if secondary_languages:
        all_languages.extend(secondary_languages)

    async for result in stream_with_language(
        audio_chunks=audio_chunks,
        project_id=project_id,
        language_codes=all_languages,
        enable_punctuation=enable_punctuation,
    ):
        yield result


def create_language_config(
    languages: list[str],
    punctuation: bool = True,
    profanity_filter: bool = False,
) -> cloud_speech.RecognitionConfig:
    """
    Create a RecognitionConfig with language and punctuation for Google Cloud Speech-to-Text.

    Uses google-cloud-speech v2 types from google.cloud.speech_v2.types.cloud_speech.
    """
    return cloud_speech.RecognitionConfig(
        language_codes=languages,
        model="latest_long",
        automatic_punctuation=punctuation,
        enable_word_time_offsets=True,
        profanity_filter=profanity_filter,
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
    )
