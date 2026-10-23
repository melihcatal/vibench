import asyncio
import websockets
import json
import os

# Use IBM Watson Speech-to-Text WebSocket
# Credentials: IBM_STT_APIKEY, IBM_STT_URL


async def microphone_stream():
    # Assume microphone audio captured elsewhere and sent as bytes
    uri = os.getenv("IBM_STT_URL")
    async with websockets.connect(uri) as ws:
        # Send initial handshake with audio format
        handshake = {"action": "start", "content-type": "audio/l16; rate=16000"}
        await ws.send(json.dumps(handshake))
        print("Microphone stream started")
        try:
            while True:  # In a real implementation, read audio chunks from the mic
                audio_chunk = b"audio_data..."  # Replace with actual microphone read
                if not audio_chunk:
                    break
                await ws.send(audio_chunk)
                # Receive response from server
                resp = await ws.recv()
                data = json.loads(resp)
                if "results" in data:
                    for result in data["results"]:
                        print("Interim:", result.get("transcript", ""))
        except websockets.ConnectionClosed:
            print("Stream closed")


if __name__ == "__main__":
    asyncio.run(microphone_stream())
