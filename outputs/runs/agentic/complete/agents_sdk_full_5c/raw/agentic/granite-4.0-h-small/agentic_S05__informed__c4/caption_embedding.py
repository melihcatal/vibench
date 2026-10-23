# [LATER-STEP] caption_embedding.py
# Embed caption chunks for semantic meeting search using Azure OpenAI Embeddings API (REST)
import asyncio
import aiohttp
import json
import os

# Provider identifier
PROVIDER = "azure_openai"

# Azure OpenAI environment variables
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
MODEL_ID = "text-embedding-ada-002"  # Azure's embedding model

async def embed_text(text: str) -> list[float]:
    """Send text to Azure OpenAI Embeddings endpoint and return embedding vector."""
    url = f"{AZURE_OPENAI_ENDPOINT}/openai/embeddings/v1"
    headers = {
        "api-key": AZURE_OPENAI_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_ID,
        "prompt": text
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            resp.raise_for_status()
            data = await resp.json()
            embeddings = data["data"][0]["embedding"]
            return embeddings

async def batch_embed(captions: list[str]) -> list[list[float]]:
    """Embed a list of caption chunks sequentially (simplified batching)."""
    vectors = []
    for cap in captions:
        vec = await embed_text(cap)
        vectors.append(vec)
    return vectors

if __name__ == "__main__":
    demo_captions = ["Project kickoff was successful.", "Next steps include reviewing metrics."]
    vectors = asyncio.run(batch_embed(demo_captions))
    print("Embeddings per caption:", len(vectors), vectors[0][:5] if vectors else [])