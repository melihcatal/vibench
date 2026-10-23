"""Start a streaming recognizer with language and punctuation settings using Google Cloud Speech-to-Text."""

from typing import AsyncIterator, Iterator, Optional, List, Tuple

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types as speech_types

from speech_client import get_speech_client, build_streaming_config
from partial_results import handle_recognition_event

ENCODING = speech_types.RecognitionConfig.AudioEncoding.LINEAR16


def start_streaming_recognizer_with_language(
    audio_chunks: Iterator[bytes],
    language_code: str = "en-US",
    alternative_language_codes: Optional[List[str]] = None,
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    enable_word_confidence: bool = True,
    model: str = "default",
    sample_rate_hertz: int = 16000,
    max_alternatives: int = 1,
    profanity_filter: bool = False,
) -> Iterator[Tuple[str, bool, float]]:
    """Start a Google Cloud Speech streaming recognizer with language and punctuation settings.

    Configures and runs a streaming recognition session with explicit language
    code, punctuation, and model settings via the Google Cloud Speech-to-Text API.

    Args:
        audio_chunks: Iterator yielding raw audio bytes.
        language_code: Primary BCP-47 language code (e.g., 'en-US', 'es-ES').
        alternative_language_codes: Additional language codes to consider.
        enable_automatic_punctuation: Add punctuation to transcripts.
        enable_word_time_offsets: Include per-word timing information.
        enable_word_confidence: Include per-word confidence scores.
        model: Recognition model to use (default, video, phone_call, command_and_search).
        sample_rate_hertz: Audio sample rate in Hz.
        max_alternatives: Maximum number of alternative hypotheses to return.
        profanity_filter: Filter profanity from transcripts.

    Yields:
        Tuples of (transcript, is_final, confidence) from the streaming API.
    """
    client = get_speech_client()

    config_params = {
        "language_code": language_code,
        "encoding": ENCODING,
        "sample_rate_hertz": sample_rate_hertz,
        "enable_automatic_punctuation": enable_automatic_punctuation,
        "enable_word_time_offsets": enable_word_time_offsets,
        "enable_word_confidence": enable_word_confidence,
        "model": model,
        "max_alternatives": max_alternatives,
        "use_enhanced": True,
    }

    if alternative_language_codes:
        config_params["alternative_language_codes"] = alternative_language_codes

    if profanity_filter:
        config_params["profanity_filter"] = True

    config = build_streaming_config(**config_params)

    streaming_config = speech_types.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
        single_utterance=False,
    )

    requests = (
        speech_types.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_chunks
    )

    responses = client.streaming_recognize(
        config=streaming_config,
        requests=requests,
    )

    for response in responses:
        for result in response.results:
            for transcript, is_final, confidence in handle_recognition_event(result):
                yield transcript, is_final, confidence
