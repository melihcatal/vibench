import asyncio
import aiohttp
import json
from speech_client import SpeechClient
from speech_models import SpeechModels

# Cohere Embed API (service=Cohere Embed API)
# SDK: cohere
# Auth: COHERE_API_KEY

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise ValueError("Environment variable COHERE_API_KEY not set")


async def embed_captions():
    """
    Streams captions via SpeechClient (e.g., Google) and embeds each chunk using Cohere.
    Yields (index, embedding) tuples.
    """
    client = SpeechClient("google")
    cohere = cohere.Client(COHERE_API_KEY)
    index = 0
    async for chunk in client.stream_microphone():
        caption = client._normalize_response(chunk)
        if not caption:
            continue
        response = cohere.embeddings.create(
            model="embed-english-v3.0",
            texts=[caption],
        )
        embedding = response.embeddings[0].embedding
        yield index, embedding
        index += 1


if __name__ == "__main__":

    async def demo():
        async for i, emb in embed_captions():
            print(f"Caption {i} embedding: {emb[:5]}...")
            await asyncio.sleep(0.5)

    asyncio.run(demo())
