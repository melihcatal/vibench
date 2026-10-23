import asyncio
import os

from google.cloud import speech_v2
from google.cloud.speech_v2 import types

from speech_client import get_speech_client, get_recognizer_resource_name

# For demonstration, we'll use a dummy audio file or simulated chunks
# In a real scenario, this would come from an actual async audio source (e.g., a network stream)

async def async_audio_chunk_source(audio_file_path: str, chunk_size_bytes: int = 3200):
    """Simulates an asynchronous audio chunk source from a file."""
    if not os.path.exists(audio_file_path):
        print(f"Warning: Audio file not found at {audio_file_path}. Generating dummy chunks.")
        # Generate dummy chunks if file not found
        for _ in range(10):
            yield b'\x00' * chunk_size_bytes # Silent dummy chunk
            await asyncio.sleep(0.1)
        return

    with open(audio_file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size_bytes)
            if not chunk:
                break
            yield chunk
            await asyncio.sleep(0.05) # Simulate async delay

async def stream_audio_chunks(audio_source_generator):
    client = get_speech_client()
    recognizer_name = get_recognizer_resource_name()

    config = types.RecognitionConfig(
        encoding=types.RecognitionConfig.AudioEncoding.LINEAR16, # Assuming 16-bit PCM
        sample_rate_hertz=16000, # Assuming 16 kHz sample rate
        language_codes=["en-US"],
        model="latest_short",
    )
    streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)

    async def request_generator():
        yield types.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for chunk in audio_source_generator:
            yield types.StreamingRecognizeRequest(audio=chunk)

    responses = client.streaming_recognize(requests=request_generator())
    async for response in responses:
        if response.results:
            for result in response.results:
                if result.alternatives:
                    yield result.alternatives[0].transcript, result.is_final

async def main():
    # Replace 'path/to/your/audio.wav' with a real 16-bit, 16kHz, mono WAV file for best results
    # Or let it generate dummy silent chunks
    audio_file = "dummy_audio.wav" # Placeholder
    print(f"Streaming from simulated source ({audio_file})...")
    async for transcript, is_final in stream_audio_chunks(async_audio_chunk_source(audio_file)):
        status = " (Final)" if is_final else " (Partial)"
        print(f"Transcript: {transcript}{status}")

if __name__ == "__main__":
    asyncio.run(main())
