# stream_microphone.py
# [SAME-SCENARIO]
# Streams microphone audio and yields interim transcripts using Deepgram Streaming API

import asyncio
import deepgram
import pyaudio

# Deepgram authentication
DEEPGRAM_API_KEY = "${DEEPGRAM_API_KEY}"

# Audio configuration
CHUNK_SIZE = 4096  # bytes
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


async def stream_microphone():
    # Initialize Deepgram client
    client = deepgram.client.Client(DEEPGRAM_API_KEY)

    # Start streaming recognizer with interim results
    recognizer = client.streaming_recognize(
        model="nvidia_large", language="en", punctuate=False, interim_results=True
    )

    # Prepare PyAudio stream
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    async def listen():
        while True:
            try:
                data = stream.read(CHUNK_SIZE)
                if not data:
                    break
                # Submit audio chunk to Deepgram
                response = await recognizer.send(data)
                if response.get("results"):
                    for result in response["results"]:
                        if result.get("alternatives"):
                            transcript = result["alternatives"][0].get("transcript", "")
                            print("Interim:", transcript)
            except asyncio.CancelledError:
                break

    # Run the listener coroutine
    await listen()


if __name__ == "__main__":
    asyncio.run(stream_microphone())
