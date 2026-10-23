# [SAME-SCENARIO] stream_microphone.py
# Streams microphone audio and yields interim transcripts using Deepgram Streaming API
import asyncio
import pyaudio
import json
import deepgram

# Deepgram authentication
DEEPGRAM_API_KEY = "${DEEPGRAM_API_KEY}"

# Microphone stream settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


async def stream_microphone():
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    async def generator():
        while True:
            data = stream.read(CHUNK)
            # Encode audio to base64 and send to Deepgram for streaming
            response = deepgram.listen(
                audio=open("data:audio/wav;base64," + data.encode("base64"), "rb"),
                model="nova",
                # Deepgram expects base64 string, use SDK method accordingly
            )
            if "results" in response:
                for result in response["results"]:
                    if "interim" in result:
                        yield result["interim"]

    yield from generator()


if __name__ == "__main__":
    asyncio.run(stream_microphone())
