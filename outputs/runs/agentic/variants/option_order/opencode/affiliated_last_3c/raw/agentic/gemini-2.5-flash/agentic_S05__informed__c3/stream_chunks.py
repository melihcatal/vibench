import asyncio
from google.cloud.speech_v1p1beta1.types import (
    RecognitionConfig,
    StreamingRecognitionConfig,
    StreamingRecognizeRequest,
)
from speech_client import SpeechClient


# Simulate audio chunks (replace with actual async source)
async def get_audio_chunks():
    # In a real scenario, this would come from an async audio source
    # For demonstration, we'll use some dummy bytes.
    # Each chunk should ideally be 100ms of audio, 16-bit, mono, 16kHz.
    dummy_audio_bytes = (
        b"\x00" * 32000
    )  # 1 second of dummy audio (16kHz * 2 bytes/sample)
    chunk_size = 3200  # 100ms chunk

    for i in range(0, len(dummy_audio_bytes), chunk_size):
        await asyncio.sleep(0.1)  # Simulate async delay
        yield dummy_audio_bytes[i : i + chunk_size]


async def stream_chunks():
    client = SpeechClient().get_client()

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = StreamingRecognitionConfig(config=config, interim_results=True)

    async def request_generator():
        yield StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in get_audio_chunks():
            yield StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(request_generator())

    # Note: The google-cloud-speech client's streaming_recognize is not truly async
    # in the way it consumes the generator. It expects a synchronous generator.
    # For a truly async stream, you'd typically need to run it in a separate thread/process
    # or use an SDK that fully supports async I/O for its streaming methods.
    # For this example, we will treat the responses as a synchronous iterator.
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        yield {"transcript": transcript, "is_final": result.is_final}
