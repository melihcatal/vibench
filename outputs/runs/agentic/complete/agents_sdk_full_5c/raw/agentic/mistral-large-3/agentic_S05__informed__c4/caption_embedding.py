import os
from sentence_transformers import SentenceTransformer
from typing import List

class DashScopeEmbeddingClient:
    def __init__(self):
        self.model = SentenceTransformer('dashscope/bge-small-en-v1.5')

    def embed(self, text: str) -> List[float]:
        return self.model.encode(text).tolist()

async def embed_caption_chunks(caption_stream):
    embedder = DashScopeEmbeddingClient()
    async for caption in caption_stream:
        embedding = embedder.embed(caption)
        print(f"Embedding for: {caption[:50]}...")
        yield embedding