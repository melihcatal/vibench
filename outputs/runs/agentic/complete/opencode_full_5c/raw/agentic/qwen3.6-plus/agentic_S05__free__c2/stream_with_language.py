from typing import AsyncIterator, List, Optional

from google.cloud import speech_v2
from google.cloud.speech_v2.types import cloud_speech

from speech_client import load_config, build_recognizer_path, validate_config
from speech_models import StreamingRecognitionResult, WordInfo


def build_language_config(
    language_codes: List[str],
    enable_automatic_punctuation: bool = True,
    model: str = "latest_long",
    max_alternatives: int = 1,
    profanity_filter: bool = False,
) -> cloud_speech.StreamingRecognitionConfig:
    return cloud_speech.StreamingRecognitionConfig(
        config=cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            language_codes=language_codes,
            model=model,
            max_alternatives=max_alternatives,
            features=cloud_speech.RecognitionFeatures(
                enable_automatic_punctuation=enable_automatic_punctuation,
                enable_word_time_offsets=True,
                profanity_filter=profanity_filter,
            ),
        ),
    )


async def stream_with_language(
    audio_source: AsyncIterator[bytes],
    language_codes: List[str] = None,
    enable_automatic_punctuation: bool = True,
    model: str = "latest_long",
    profanity_filter: bool = False,
) -> AsyncIterator[StreamingRecognitionResult]:
    if language_codes is None:
        language_codes = ["en-US"]

    config = load_config()
    validate_config(config)

    client = speech_v2.SpeechClient()
    recognizer = build_recognizer_path(config)

    streaming_config = build_language_config(
        language_codes=language_codes,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model=model,
        profanity_filter=profanity_filter,
    )

    async def request_generator():
        yield cloud_speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_source:
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)
        yield cloud_speech.StreamingRecognizeRequest(audio=b"")

    responses = client.streaming_recognize(
        recognizer=recognizer,
        requests=request_generator(),
    )

    for response in responses:
        for result in response.results:
            words = [
                WordInfo(
                    word=w.word,
                    start_offset_seconds=w.start_offset.seconds
                    + w.start_offset.microseconds / 1_000_000,
                    end_offset_seconds=w.end_offset.seconds
                    + w.end_offset.microseconds / 1_000_000,
                    confidence=w.confidence,
                )
                for w in result.word_info
            ]
            yield StreamingRecognitionResult(
                transcript=result.alternatives[0].transcript,
                is_final=result.is_final,
                stability=result.stability,
                confidence=result.alternatives[0].confidence,
                words=words,
                language_code=language_codes[0],
            )
