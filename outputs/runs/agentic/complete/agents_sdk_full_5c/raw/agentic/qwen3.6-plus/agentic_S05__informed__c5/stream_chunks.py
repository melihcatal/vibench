"""Streams audio chunks from an async source via Google Cloud Speech-to-Text streaming API."""

from typing import AsyncIterator, AsyncGenerator
from google.cloud.speech_v2.types import cloud_speech
from speech_client import get_speech_client, build_recognizer_path
from speech_models import StreamingSpeechResult, normalize_recognition_result


async def build_request_stream(
    recognizer: str,
    audio_chunks: AsyncIterator[bytes],
    language_codes: list[str] | None = None,
    model: str = "latest_long",
) -> AsyncIterator[cloud_speech.StreamingRecognizeRequest]:
    """Build streaming requests for google-cloud-speech SDK with config followed by audio chunks."""
    codes = language_codes or ["en-US"]
    yield cloud_speech.StreamingRecognizeRequest(
        recognizer=recognizer,
        streaming_config=cloud_speech.StreamingRecognitionConfig(
            config=cloud_speech.RecognitionConfig(
                language_codes=codes,
                model=model,
                automatic_punctuation=True,
                enable_word_time_offsets=True,
                auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            ),
        ),
    )
    async for chunk in audio_chunks:
        if chunk:
            yield cloud_speech.StreamingRecognizeRequest(audio=chunk)


async def stream_audio_chunks(
    audio_chunks: AsyncIterator[bytes],
    project_id: str,
    language_code: str = "en-US",
) -> AsyncGenerator[StreamingSpeechResult, None]:
    """
    Stream audio chunks from an async source through Google Cloud Speech-to-Text streaming API.

    Uses google-cloud-speech SDK streaming_recognize with speech.googleapis.com endpoint.
    Model: latest_long.
    """
    recognizer = build_recognizer_path(project_id=project_id)
    client = get_speech_client()

    request_stream = build_request_stream(
        recognizer=recognizer,
        audio_chunks=audio_chunks,
        language_codes=[language_code],
    )

    responses = client.streaming_recognize(requests=request_stream)

    for response in responses:
        for result in response.results:
            normalized = normalize_recognition_result(result)
            yield normalized


async def stream_audio_chunks_with_config(
    audio_chunks: AsyncIterator[bytes],
    project_id: str,
    language_codes: list[str] | None = None,
    model: str = "latest_long",
    enable_punctuation: bool = True,
) -> AsyncGenerator[StreamingSpeechResult, None]:
    """
    Stream audio chunks with full configuration control via Google Cloud Speech-to-Text.

    Uses google-cloud-speech SDK with speech.googleapis.com.
    """
    recognizer = build_recognizer_path(project_id=project_id)
    client = get_speech_client()
    codes = language_codes or ["en-US"]

    request_stream = build_request_stream(
        recognizer=recognizer,
        audio_chunks=audio_chunks,
        language_codes=codes,
        model=model,
    )

    responses = client.streaming_recognize(requests=request_stream)

    for response in responses:
        for result in response.results:
            normalized = normalize_recognition_result(result)
            yield normalized
