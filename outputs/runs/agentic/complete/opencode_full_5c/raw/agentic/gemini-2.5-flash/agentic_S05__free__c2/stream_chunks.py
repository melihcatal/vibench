import asyncio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client, get_streaming_config

# Audio recording parameters (example)
RATE = 16000
CHUNK_SIZE = int(RATE / 10)  # 100ms chunks


async def stream_audio_chunks(audio_chunk_source):
    """Streams audio chunks from an async source to Google Speech-to-Text and yields transcripts.

    Args:
        audio_chunk_source: An async generator or similar that yields audio chunks (bytes).
    """
    client = get_speech_client()
    streaming_config = get_streaming_config()

    async def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_chunk_source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = await client.streaming_recognize(request_generator())

    async for response in responses:
        if not response.results:
            continue

        for result in response.results:
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            is_final = result.is_final
            yield transcript, is_final


# Example of an async audio chunk source (for demonstration)
async def simulate_audio_source(num_chunks=50, chunk_duration_ms=100):
    # Simulate silence for demonstration purposes
    silent_chunk = b"\x00" * CHUNK_SIZE * 2  # 16-bit mono audio
    for _ in range(num_chunks):
        await asyncio.sleep(chunk_duration_ms / 1000.0)
        yield silent_chunk
