from typing import AsyncIterator, AsyncIterable

from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech

from speech_client import SpeechConfig, build_speech_client, build_recognition_config
from speech_models import (
    StreamingResult,
    normalize_streaming_result,
    build_streaming_event,
    StreamingEvent,
)


def build_language_config(
    language_code: str = "en-US",
    additional_languages: list[str] | None = None,
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    profanity_filter: bool = False,
    model: str = "latest_long",
) -> SpeechConfig:
    return SpeechConfig(
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
        profanity_filter=profanity_filter,
        model=model,
    )


async def stream_with_language(
    audio_source: AsyncIterable[bytes],
    language_code: str = "en-US",
    additional_languages: list[str] | None = None,
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    profanity_filter: bool = False,
    model: str = "latest_long",
    config: SpeechConfig | None = None,
) -> AsyncIterator[StreamingEvent]:
    cfg = config or build_language_config(
        language_code=language_code,
        additional_languages=additional_languages,
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
        profanity_filter=profanity_filter,
        model=model,
    )

    client = build_speech_client(cfg)
    recognition_config = build_recognition_config(cfg)

    language_codes = [cfg.language_code]
    if additional_languages:
        language_codes.extend(additional_languages)
    recognition_config.language_codes = language_codes

    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=recognition_config
    )

    async def request_generator():
        yield cloud_speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_source:
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    responses = client.streaming_recognize(requests=request_generator())

    for response in responses:
        for result in response.results:
            normalized = normalize_streaming_result(result)
            event_type = "final" if normalized.is_final else "interim"
            yield build_streaming_event(event_type=event_type, result=normalized)
