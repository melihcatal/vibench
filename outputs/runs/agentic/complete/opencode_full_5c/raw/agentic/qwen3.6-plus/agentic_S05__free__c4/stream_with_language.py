from typing import AsyncGenerator, Optional, List

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

from speech_client import (
    create_speech_client,
    build_streaming_config,
    GOOGLE_SPEECH_API_ENDPOINT,
    DEFAULT_MODEL,
)
from speech_models import (
    RecognitionResult,
    normalize_google_response,
    StreamConfig,
)


def build_language_config(
    project_id: str,
    language_code: str = "en-US",
    additional_languages: Optional[List[str]] = None,
    model: str = DEFAULT_MODEL,
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    profanity_filter: bool = False,
    max_alternatives: int = 1,
    enable_spoken_punctuation: bool = True,
    location: str = "global",
) -> dict:
    from google.cloud.speech_v2.types import cloud_speech

    recognizer = f"projects/{project_id}/locations/{location}/recognizers/_"

    language_codes = [language_code]
    if additional_languages:
        language_codes.extend(additional_languages)

    features = cloud_speech.RecognitionFeatures(
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
        profanity_filter=profanity_filter,
        max_alternatives=max_alternatives,
        enable_spoken_punctuation=enable_spoken_punctuation,
    )

    config = cloud_speech.RecognitionConfig(
        model=model,
        language_codes=language_codes,
        features=features,
    )

    streaming_features = cloud_speech.StreamingRecognitionFeatures(
        interim_results=True,
        voice_activity_timeout=cloud_speech.StreamingRecognitionFeatures.VoiceActivityTimeout(
            speech_start_timeout="5s",
            speech_end_timeout="3s",
        ),
    )

    return {
        "recognizer": recognizer,
        "config": config,
        "streaming_features": streaming_features,
        "language_codes": language_codes,
    }


async def stream_with_language_settings(
    audio_chunks,
    project_id: str,
    language_code: str = "en-US",
    additional_languages: Optional[List[str]] = None,
    model: str = DEFAULT_MODEL,
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    profanity_filter: bool = False,
    max_alternatives: int = 1,
) -> AsyncGenerator[RecognitionResult, None]:
    client = create_speech_client()

    config = build_language_config(
        project_id=project_id,
        language_code=language_code,
        additional_languages=additional_languages,
        model=model,
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
        profanity_filter=profanity_filter,
        max_alternatives=max_alternatives,
    )

    def request_generator():
        yield cloud_speech.StreamingRecognizeRequest(
            recognizer=config["recognizer"],
            streaming_config=config["config"],
        )
        for chunk in audio_chunks:
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)

    responses = client.streaming_recognize(requests=request_generator())

    for response in responses:
        if response.results:
            result = normalize_google_response(response)
            yield result


async def stream_multilingual(
    audio_chunks,
    project_id: str,
    primary_language: str = "en-US",
    secondary_languages: Optional[List[str]] = None,
    model: str = "latest_long",
) -> AsyncGenerator[RecognitionResult, None]:
    async for result in stream_with_language_settings(
        audio_chunks=audio_chunks,
        project_id=project_id,
        language_code=primary_language,
        additional_languages=secondary_languages,
        model=model,
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True,
        profanity_filter=False,
    ):
        yield result
