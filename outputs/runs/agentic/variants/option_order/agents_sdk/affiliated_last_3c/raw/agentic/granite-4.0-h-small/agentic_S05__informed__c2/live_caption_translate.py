import json
import asyncio
import sys
from typing import AsyncIterable

from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource

# Load credentials from local helper (speech_client.py)
config = load_config()
STT_APIKEY = config["IBM_STT_APIKEY"]
STT_URL = config["IBM_STT_URL"]

async def stream_recognizer(audio_stream: AsyncIterable[bytes]):
    """Stream audio to IBM Watson Speech-to-Text WebSocket and print results using asyncio.""",
    service = SpeechToTextV1(authenticator=APIKeyAuthenticator(STT_APIKEY), url=STT_URL)

    class AsyncRecognizeCallback(RecognizeCallback):
        def __init__(self):
            self.on_data = asyncio.Event()
            self.results = []

        def on_data(self, data):
            self.results.append(data)
            self.on_data.set()

        def on_connected(self):
            pass

        def on_error(self, error):
            print("Error received:", error)

        def on_close(self):
            pass

    callback = AsyncRecognizeCallback()
    audio_source = AudioSource(audio_stream)
    service.recognize_using_websocket(audio=audio_source, content_type="audio/l16; rate=16000",
                                      recognize_callback=callback, interim_results=True)
    # Wait for inbound data packets
    while True:
        await callback.on_data.wait()
        data = callback.results.pop()
        print("Watson interim result:", data)

if __name__ == "__main__":
    # Simple example that reads 1024‑byte chunks from stdin
    async def stdin_source():
        while True:
            chunk = sys.stdin.buffer.read(1024)
            if not chunk:
                break
            yield chunk
    asyncio.run(stream_recognizer(stdin_source()))
