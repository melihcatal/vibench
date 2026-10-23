import asyncio
from typing import AsyncGenerator, AsyncIterable, List, Optional

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

from speech_client import SpeechConfig, create_speech_client, build_recognition_config
from speech_models import StreamingTranscriptEvent, normalize_streaming_event


async def start_streaming_recognizer(
    audio_source: AsyncIterable[bytes],
    language_code: str = "en-US",
    enable_punctuation: bool = True,
    model: str = "latest_long",
    config: Optional[SpeechConfig] = None,
    additional_language_codes: Optional[List[str]] = None,
    enable_spoken_punctuation: bool = False,
    enable_word_time_offsets: bool = True,
    enable_word_confidence: bool = True,
    profanity_filter: bool = False,
    max_alternatives: int = 1,
) -> AsyncGenerator[StreamingTranscriptEvent, None]:
    if config is None:
        config = SpeechConfig.from_env()

    config.language_code = language_code
    config.model = model
    config.enable_automatic_punctuation = enable_punctuation
    config.enable_spoken_punctuation = enable_spoken_punctuation
    config.enable_word_time_offsets = enable_word_time_offsets
    config.enable_word_confidence = enable_word_confidence
    config.profanity_filter = profanity_filter
    config.max_alternatives = max_alternatives

    client = create_speech_client(config)
    recognition_config = build_recognition_config(config)

    language_codes = [language_code]
    if additional_language_codes:
        language_codes.extend(additional_language_codes)

    recognition_config.language_codes.clear()
    for lang in language_codes:
        recognition_config.language_codes.append(lang)

    recognition_config.features.enable_automatic_punctuation = enable_punctuation
    recognition_config.features.enable_spoken_punctuation = enable_spoken_punctuation
    recognition_config.features.enable_word_time_offsets = enable_word_time_offsets
    recognition_config.features.enable_word_confidence = enable_word_confidence
    recognition_config.features.profanity_filter = profanity_filter
    recognition_config.features.max_alternatives = max_alternatives
    recognition_config.model = model

    streaming_config = cloud_speech.StreamingRecognitionConfig(
        config=recognition_config,
        streaming_features=cloud_speech.StreamingRecognitionFeatures(
            enable_voice_activity_events=True,
            interim_results=True,
        ),
    )

    config_request = cloud_speech.StreamingRecognizeRequest(
        recognizer=config.recognizer_path,
        streaming_config=streaming_config,
    )

    async def request_generator():
        yield config_request
        async for chunk in audio_source:
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    responses = client.streaming_recognize(requests=request_generator())

    for response in responses:
        event = normalize_streaming_event(response)
        if event is not None:
            yield event


async def stream_with_language_hints(
    audio_source: AsyncIterable[bytes],
    primary_language: str = "en-US",
    secondary_languages: Optional[List[str]] = None,
    enable_punctuation: bool = True,
) -> AsyncGenerator[StreamingTranscriptEvent, None]:
    async for event in start_streaming_recognizer(
        audio_source=audio_source,
        language_code=primary_language,
        enable_punctuation=enable_punctuation,
        additional_language_codes=secondary_languages,
        model="latest_long",
    ):
        yield event


async def stream_with_punctuation_only(
    audio_source: AsyncIterable[bytes],
    language_code: str = "en-US",
    enable_spoken_punctuation: bool = True,
) -> AsyncGenerator[StreamingTranscriptEvent, None]:
    async for event in start_streaming_recognizer(
        audio_source=audio_source,
        language_code=language_code,
        enable_punctuation=True,
        enable_spoken_punctuation=enable_spoken_punctuation,
        model="latest_long",
    ):
        yield event
