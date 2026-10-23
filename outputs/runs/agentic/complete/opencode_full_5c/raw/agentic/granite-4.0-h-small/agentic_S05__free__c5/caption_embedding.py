# [LATER-STEP] caption_embedding.py
# Embed caption chunks for semantic meeting search using Cohere Rerank API
import asyncio
import aiohttp
from speech_models import normalize_response

# Provider identifier
PROVIDER = "cohere"

# Cohere API endpoint and key (hosted service)
COHERE_API_KEY = "YOUR_COHERE_API_KEY"
COHERE_RERANK_URL = "https://api.cohere.com/v1/rerank"


async def embed_text(text: str) -> dict:
    """Embed a single caption chunk using Cohere's rerank endpoint."""
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "queries": [text],
        "documents": ["<placeholder>"],  # placeholder, we just need embeddings
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            COHERE_RERANK_URL, headers=headers, json=payload
        ) as resp:
            data = await resp.json()
            # Embeddings returned as list of floats under documents[0].embedding
            embedding = data["documents"][0]["embedding"]
            return {
                "provider": PROVIDER,
                "embedding": embedding,
                "timestamp": caption["timestamp"],
            }


async def caption_embedding(audio_iterator) -> None:
    """Consume async caption iterator and emit embeddings for each chunk."""
    # Placeholder: in practice you would keep a store of embeddings for search
    async for caption in audio_iterator:
        emb = await embed_text(caption["transcript"])
        # For demo, just print the embedding vector
        print(f"[EMBED] {PROVIDER}: {emb['embedding'][:5]}... (truncated)")


# Example usage with stream_microphone (uncomment to test)
# async def main():
#     async for cap in stream_microphone():
#         await caption_embedding([cap])
# asyncio.run(main())
