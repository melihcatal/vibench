import asyncio
from typing import AsyncGenerator, AsyncIterable, Optional

from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

from speech_client import SpeechConfig, create_speech_client, build_recognition_config
from speech_models import StreamingTranscriptEvent, normalize_streaming_event


async def stream_chunks(
    audio_source: AsyncIterable[bytes],
    config: Optional[SpeechConfig] = None,
) -> AsyncGenerator[StreamingTranscriptEvent, None]:
    if config is None:
        config = SpeechConfig.from_env()

    client = create_speech_client(config)
    recognition_config = build_recognition_config(config)

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


async def chunked_audio_from_file(
    file_path: str, chunk_size: int = 6400, sample_rate: int = 16000
) -> AsyncGenerator[bytes, None]:
    loop = asyncio.get_event_loop()

    def read_chunk():
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    for chunk in read_chunk():
        yield chunk
        await asyncio.sleep(chunk_size / (sample_rate * 2 * 1000))


async def chunked_audio_from_buffer(
    buffer: asyncio.Queue, chunk_timeout: float = 0.1
) -> AsyncGenerator[bytes, None]:
    while True:
        try:
            chunk = await asyncio.wait_for(buffer.get(), timeout=chunk_timeout)
            if chunk is None:
                break
            yield chunk
        except asyncio.TimeoutError:
            continue
