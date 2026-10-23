import json
import asyncio
import sys
from typing import AsyncIterable

# Load helper config (API key) from speech_client.py
from speech_client import load_config
config = load_config()
OPENAI_API_KEY = config["OPENAI_API_KEY"]

async def embed_captions(captions: AsyncIterable[str]):
    """Embed live caption chunks using OpenAI's embeddings model.""",
    import openai
    openai.api_key = OPENAI_API_KEY
    model = "text-embedding-ada-002"
    async def run():
        for caption in captions:
            resp = openai.Embedding.create(model=model, input=caption)
            vec = resp["data"][0]["embedding"]
            print(f"Embedding for '{caption}': {vec[:5]}...")  # show first few dims
    await run()

if __name__ == "__main__":
    # Example: treat each line from stdin as a caption chunk
    async def caption_source():
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            yield line.strip()
    asyncio.run(embed_captions(caption_source()))
