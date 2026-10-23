# [SAME-SCENARIO] stream_microphone.py
# Streams microphone audio using Deepgram Streaming API and yields interim transcripts
import asyncio
import pyaudio
import deepgram

# Provider identifier
PROVIDER = "deepgram"

# Configuration
DEEPGRAM_API_KEY = "${DEEPGRAM_API_KEY}"  # set your API key in environment
CHUNK_SIZE = 4096  # bytes per audio chunk

async def microphone_stream():
    pa = pyaudio.PyAudio()
    # 16000 Hz, 16-bit mono
    stream = pa.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=16000,
                     input=True,
                     frames_per_buffer=CHUNK_SIZE)

    async def generate_audio():
        while True:
            data = stream.read(CHUNK_SIZE)
            if not data:
                break
            yield data

    async for audio_chunk in generate_audio():
        # Send chunk to Deepgram streaming endpoint
        client = deepgram.transcription.StreamingClient(DEEPGRAM_API_KEY)
        async with client.stream(
            model="noha",
            language="en",
            punctuation_enabled=True,
            interim_results=True
        ) as s:
            async for result in s.transcribe(audio_chunk):
                if result.get("partial"):
                    yield result["partial"]

    stream.stop_stream()
    stream.close()
    pa.terminate()

if __name__ == "__main__":
    asyncio.run(microphone_stream())