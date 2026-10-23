import asyncio
import base64
from speech_client import get_transcriber

# Simulate an asynchronous source of audio chunks (e.g., a WebSocket)
async def async_audio_chunk_generator():
    """
    An async generator that yields audio chunks.
    This simulates receiving audio data over a network.
    """
    # A silent 1-second WAV file chunk, encoded in base64
    silent_chunk_base64 = "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAAABkYXRhIAAAAAA="
    chunk_data = base64.b64decode(silent_chunk_base64)
    
    for _ in range(10):
        await asyncio.sleep(0.5)  # Simulate network latency
        yield chunk_data


async def stream_from_async_source():
    """
    Connects to AssemblyAI and streams audio chunks from an async generator.
    """
    transcriber = get_transcriber()
    results = []

    def on_final_transcript(transcript):
        print(f"Final transcript: {transcript.text}")
        results.append(transcript.text)
    
    transcriber.on_final_transcript = on_final_transcript

    await transcriber.connect_async()

    async for chunk in async_audio_chunk_generator():
        await transcriber.stream_async(chunk)

    await transcriber.close_async()
    return results
