import asyncio
import websockets
import json
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_text(text):
    """Embeds caption chunk using SentenceTransformer provider."""
    embeddings = model.encode(text)
    # Return as list for easier transport; shape (768,)
    return embeddings.tolist()

async def embed_captions(stream_uri='wss://api.example.com/stream'):
    """Embeds live caption chunks for semantic search."""
    async with websockets.connect(stream_uri) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if 'partial' in data or 'final' in data:
                text = data.get('partial', '')
                if text:
                    embedding = embed_text(text)
                    print('Embedding:', embedding[:5], '...')