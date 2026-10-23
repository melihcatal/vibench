from sentence_transformers import SentenceTransformer
import numpy as np
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    embedding = model.encode(text, convert_to_tensor=True)
    return embedding.cpu().numpy()

async def embed_caption_chunks(caption_generator):
    async for caption in caption_generator:
        embedding = embed_text(caption)
        print(f"Embedding shape for '{caption[:20]}...': {embedding.shape}")
        yield embedding