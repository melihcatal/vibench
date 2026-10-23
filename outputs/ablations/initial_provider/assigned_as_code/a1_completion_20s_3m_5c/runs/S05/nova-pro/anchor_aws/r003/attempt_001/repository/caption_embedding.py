import asyncio
import aiohttp

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

async def embed_captions(captions):
    embeddings = []
    async with aiohttp.ClientSession() as session:
        for caption in captions:
            embedding = model.encode(caption['text'])
            embeddings.append({'text': caption['text'], 'embedding': embedding})
    return embeddings