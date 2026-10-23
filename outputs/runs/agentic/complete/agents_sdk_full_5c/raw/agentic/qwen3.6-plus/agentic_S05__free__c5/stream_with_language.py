"""Start a streaming recognizer with language and punctuation settings using Google Cloud Speech-to-Text.

Provider: Google Cloud Speech-to-Text (speech.googleapis.com)
SDK: google-cloud-speech (google.cloud.speech_v1p1beta1)
Models: default, command_and_search, phone_call, video, medical_conversation
"""

from typing import Generator, Optional

from google.cloud import speech_v1p1beta1 as speech

from speech_client import create_speech_client, build_config_with_language
from speech_models import StreamingTranscriptResult, normalize_transcript_text


def start_streaming_with_language(
    audio_source: Generator[bytes, None, None],
    language_code: str = "en-US",
    alternative_language_codes: Optional[list[str]] = None,
    enable_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    model: str = "default",
    sample_rate_hertz: int = 16000,
) -> Generator[StreamingTranscriptResult, None, None]:
    """Start a streaming recognizer with explicit language and punctuation settings.

    Uses google-cloud-speech SDK to connect to speech.googleapis.com.

    Provider: Google Cloud Speech-to-Text
    Models:
        - 'default': Best for general speech
        - 'command_and_search': Best for short commands/search queries
        - 'phone_call': Optimized for phone audio
        - 'video': Optimized for video/audio content
        - 'medical_conversation': Medical domain

    Args:
        audio_source: Generator yielding LINEAR16 PCM audio bytes
        language_code: Primary BCP-47 language code (e.g., 'en-US', 'es-ES', 'fr-FR')
        alternative_language_codes: Additional languages to detect
        enable_punctuation: Enable automatic punctuation insertion
        enable_word_time_offsets: Include word-level timing information
        model: Google Cloud Speech model identifier
        sample_rate_hertz: Audio sample rate

    Yields:
        StreamingTranscriptResult objects with interim and final results
    """
    client = create_speech_client()
    streaming_config = build_config_with_language(
        language_code=language_code,
        alternative_language_codes=alternative_language_codes,
        enable_automatic_punctuation=enable_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
        model=model,
        sample_rate_hertz=sample_rate_hertz,
    )

    def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        for chunk in audio_source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(requests=request_generator())

    for response in responses:
        if not response.results:
            continue
        for result in response.results:
            transcript_result = StreamingTranscriptResult.from_google_result(result)
            transcript_result.transcript = normalize_transcript_text(
                transcript_result.transcript
            )
            yield transcript_result


def start_streaming_multilingual(
    audio_source: Generator[bytes, None, None],
    primary_language: str = "en-US",
    secondary_languages: Optional[list[str]] = None,
    enable_punctuation: bool = True,
) -> Generator[StreamingTranscriptResult, None, None]:
    """Start multilingual streaming recognition with Google Cloud Speech-to-Text.

    Provider: Google Cloud Speech-to-Text (speech.googleapis.com)

    Supports up to 3 additional language codes for mixed-language audio.

    Args:
        audio_source: Generator yielding audio bytes
        primary_language: Primary BCP-47 language code
        secondary_languages: List of secondary language codes (max 3)
        enable_punctuation: Enable automatic punctuation

    Yields:
        StreamingTranscriptResult objects
    """
    if secondary_languages and len(secondary_languages) > 3:
        secondary_languages = secondary_languages[:3]

    yield from start_streaming_with_language(
        audio_source=audio_source,
        language_code=primary_language,
        alternative_language_codes=secondary_languages,
        enable_punctuation=enable_punctuation,
        model="default",
    )
