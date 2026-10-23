import asyncio
import websockets
import json

async def stream_chunks(audio_source):
    """Streams audio chunks from an async generator (audio_source) to a provider and yields partial transcripts."""    uri = "wss://api.example.com/stream"  # Provider endpoint
    async with websockets.connect(uri) as ws:
        from speech_client import get_stt_client
        client = get_stt_client()
        async for chunk in audio_source:
            await ws.send(chunk)
            # Process response
            resp = await ws.recv()
            data = json.loads(resp)
            if "partial" in data:
                yield data["partial"]