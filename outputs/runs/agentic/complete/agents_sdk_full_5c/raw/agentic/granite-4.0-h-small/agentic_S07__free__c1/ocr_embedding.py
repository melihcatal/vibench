import os
import numpy as np
from typing import List, Tuple
from dotenv import load_dotenv
import httpx
from sentence_transformers import SentenceTransformer
from document_models import EmbeddingRequest, EmbeddingResponse

load_dotenv()
EMBED_API_URL = os.getenv('EMBED_API_URL', 'https://api.launchcloud.com/embed')
EMBED_API_KEY = os.getenv('EMBED_API_KEY')
MODEL_ID = 'all-MiniLM-L6-v2'

def embed_sections(texts: List[str], model_name: str = MODEL_ID) -> List[np.ndarray]:
    """Embed extracted document sections for semantic retrieval using a hosted sentence transformer."""
    payload = {
        "texts": texts,
        "model": model_name
    }
    resp = httpx.post(EMBED_API_URL, json=payload, auth=(EMBED_API_KEY, ''))
    resp.raise_for_status()
    embeddings = resp.json()['embeddings']
    # Convert to numpy arrays
    return [np.array(vec, dtype=np.float32) for vec in embeddings]

async def embed_via_hosted_api(request: EmbeddingRequest) -> EmbeddingResponse:
    """Hosted API wrapper for embeddings."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            EMBED_API_URL,
            json=request.dict(),
            auth=(EMBED_API_KEY, '')
        )
        resp.raise_for_status()
        data = resp.json()
        return EmbeddingResponse(embeddings=data['embeddings'])
