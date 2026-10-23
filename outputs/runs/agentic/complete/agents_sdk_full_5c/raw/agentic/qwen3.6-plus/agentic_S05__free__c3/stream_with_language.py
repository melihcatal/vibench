"""
Start a streaming recognizer with language and punctuation settings using Google Cloud Speech-to-Text.

Configures and initiates a google.cloud.speech.SpeechClient.streaming_recognize session
with explicit language_code, enable_automatic_punctuation, and alternative language
hypotheses for multilingual or punctuation-aware recognition.
"""

from typing import Generator, Optional

from google.cloud import speech

from speech_client import create_speech_client, get_streaming_config, SpeechClientConfig
from speech_models import (
    InterimTranscript,
    FinalTranscript,
    parse_streaming_response,
    build_initial_streaming_request,
    normalize_transcript_text,
)


def build_language_aware_config(
    primary_language: str = "en-US",
    alternative_languages: Optional[list[str]] = None,
    enable_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    model: str = "latest_long",
    use_enhanced: bool = False,
    sample_rate_hertz: int = 16000,
) -> speech.StreamingRecognitionConfig:
    """
    Build a StreamingRecognitionConfig with language and punctuation settings.

    Configures google-cloud-speech with primary and alternative language codes,
    automatic punctuation, and optional enhanced model selection.

    Args:
        primary_language: Primary BCP-47 language code (e.g., "en-US").
        alternative_languages: List of additional language codes to consider.
        enable_punctuation: Enable automatic punctuation.
        enable_word_time_offsets: Include word-level timing.
        model: Google model ID (latest_long, latest_short, phone_call, video, command_and_search).
        use_enhanced: Use an enhanced model for better accuracy.
        sample_rate_hertz: Audio sample rate.

    Returns:
        Configured StreamingRecognitionConfig for Google Cloud Speech-to-Text.
    """
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=primary_language,
        enable_automatic_punctuation=enable_punctuation,
        model=model,
        use_enhanced=use_enhanced,
        enable_word_time_offsets=enable_word_time_offsets,
    )

    if alternative_languages:
        recognition_config.alternative_language_codes = alternative_languages

    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
    )


def stream_with_language(
    audio_chunks: Generator[bytes, None, None],
    primary_language: str = "en-US",
    alternative_languages: Optional[list[str]] = None,
    enable_punctuation: bool = True,
    model: str = "latest_long",
    sample_rate_hertz: int = 16000,
) -> Generator[dict, None, None]:
    """
    Start a streaming recognizer with language and punctuation settings.

    Sends audio chunks to google.cloud.speech.SpeechClient.streaming_recognize
    using a config built with the specified language codes and punctuation options.
    Yields normalized transcript events (interim and final).

    Args:
        audio_chunks: Generator yielding raw audio bytes.
        primary_language: Primary BCP-47 language code.
        alternative_languages: Additional language codes to consider.
        enable_punctuation: Enable automatic punctuation.
        model: Google recognition model ID.
        sample_rate_hertz: Audio sample rate.

    Yields:
        Dict with 'type', 'text', 'confidence', and 'raw' transcript object.
    """
    client = create_speech_client()

    streaming_config = build_language_aware_config(
        primary_language=primary_language,
        alternative_languages=alternative_languages,
        enable_punctuation=enable_punctuation,
        model=model,
        sample_rate_hertz=sample_rate_hertz,
    )

    initial_request = build_initial_streaming_request(streaming_config)

    def request_iter():
        yield initial_request
        for chunk in audio_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(
        config=streaming_config,
        requests=request_iter(),
    )

    for response in responses:
        transcripts = parse_streaming_response(response)
        for t in transcripts:
            text = normalize_transcript_text(t.text)
            result = {
                "type": "final" if isinstance(t, FinalTranscript) else "interim",
                "text": text,
                "confidence": t.confidence,
                "raw": t,
            }
            if isinstance(t, FinalTranscript):
                result["language_code"] = t.language_code
                result["word_info"] = t.word_info
            else:
                result["stability"] = t.stability
            yield result
