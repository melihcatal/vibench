# SAME-SCENARIO: stream_microphone.py
# streams microphone audio and yields interim transcripts
import asyncio
import pyaudio  # pip install pyaudio
import deepgram  # pip install deepgram-sdk-python

# Deepgram Streaming SDK imported – provider identifiable
DEEPGRAM_API_KEY = "YOUR_DEEPGRAM_API_KEY"


async def stream_microphone(url: str = "wss://api.deepgram.io/v1/stream"):
    """Stream microphone audio to Deepgram and print interim transcripts.

    Args:
        url: WebSocket endpoint for Deepgram streaming.
    """
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
    )

    async with deepgram.Stream(url, DEEPGRAM_API_KEY) as ws:
        # Send initial request payload
        init_payload = {
            "config": {
                "model": "nova",
                "language": "en",
                "punctuation": True,
                "interim_results": True,
            }
        }
        await ws.send_json(init_payload)

        while True:
            data = stream.read(1024)
            if not data:
                break
            # Send 16-bit PCM audio (little-endian)
            await ws.send_bytes(data)

            response = await ws.receive_json()
            # Deepgram returns interim and final results in the same message
            for result in response.get("results", []):
                if result.get("is_final"):
                    print(
                        "Final transcript:",
                        result.get("alternatives", [{}])[0].get("transcript"),
                    )
                else:
                    print(
                        "Interim transcript:",
                        result.get("alternatives", [{}])[0].get("transcript"),
                    )


if __name__ == "__main__":
    asyncio.run(stream_microphone())
