"""Stream audio chunks from an async source to Google Cloud Speech-to-Text.

Provider: Google Cloud Speech-to-Text (speech.googleapis.com)
SDK: google-cloud-speech (google.cloud.speech_v1p1beta1)
Uses asyncio for async audio chunk generation.
"""

import asyncio
from typing import AsyncGenerator, Generator, Optional

from google.cloud import speech_v1p1beta1 as speech

from speech_client import create_speech_client, build_streaming_config
from speech_models import StreamingTranscriptResult


async def async_audio_chunks(
    source: AsyncGenerator[bytes, None],
) -> AsyncGenerator[bytes, None]:
    """Yield audio chunks from an async source."""
    async for chunk in source:
        yield chunk


async def async_request_generator(
    audio_source: AsyncGenerator[bytes, None],
    streaming_config: speech.StreamingRecognitionConfig,
) -> AsyncGenerator[speech.StreamingRecognizeRequest, None]:
    """Generate StreamingRecognizeRequest objects from async audio chunks.

    Provider: Google Cloud Speech-to-Text (speech.googleapis.com)
    """
    yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
    async for chunk in audio_source:
        yield speech.StreamingRecognizeRequest(audio_content=chunk)


def run_streaming_recognition_sync(
    requests: Generator[speech.StreamingRecognizeRequest, None, None],
    client: speech.SpeechClient,
) -> Generator[speech.StreamingRecognizeResponse, None, None]:
    """Run streaming recognition synchronously with pre-built requests.

    Provider: Google Cloud Speech-to-Text (speech.googleapis.com)
    """
    return client.streaming_recognize(requests=requests)


async def stream_chunks_to_transcripts(
    audio_source: AsyncGenerator[bytes, None],
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    model: str = "default",
    enable_punctuation: bool = True,
) -> AsyncGenerator[StreamingTranscriptResult, None]:
    """Stream audio chunks from an async source and yield transcription results.

    Uses google-cloud-speech SDK connecting to speech.googleapis.com.
    Provider: Google Cloud Speech-to-Text
    Model: default, command_and_search, phone_call, video, medical_conversation

    Args:
        audio_source: Async generator yielding raw audio bytes (LINEAR16 PCM)
        language_code: BCP-47 language code
        sample_rate_hertz: Audio sample rate
        model: Google Cloud Speech model identifier
        enable_punctuation: Whether to enable automatic punctuation

    Yields:
        StreamingTranscriptResult objects (interim and final)
    """
    client = create_speech_client()
    streaming_config = build_streaming_config(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
        model=model,
        enable_interim_results=True,
    )

    loop = asyncio.get_event_loop()

    async def _collect_responses():
        request_gen = async_request_generator(audio_source, streaming_config)

        def _sync_recognize():
            return list(run_streaming_recognition_sync(request_gen, client))

        responses = await loop.run_in_executor(None, _sync_recognize)
        return responses

    responses = await _collect_responses()

    for response in responses:
        if not response.results:
            continue
        for result in response.results:
            transcript_result = StreamingTranscriptResult.from_google_result(result)
            yield transcript_result


async def stream_chunks_from_iterable(
    chunks: list[bytes],
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
) -> AsyncGenerator[StreamingTranscriptResult, None]:
    """Stream from a list of pre-loaded audio byte chunks.

    Provider: Google Cloud Speech-to-Text (speech.googleapis.com)
    """
    async def _chunk_source():
        for chunk in chunks:
            yield chunk

    async for result in stream_chunks_to_transcripts(
        _chunk_source(),
        language_code=language_code,
        sample_rate_hertz=sample_rate_hertz,
    ):
        yield result
