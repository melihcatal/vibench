import numpy as np
import os
from openai import Embedding
from .document_models import TextResult

def ocr_embedding(texts: List[str], model: str = 'text-embedding-3-large') -> np.ndarray:
    """Embed extracted document sections for semantic retrieval using OpenAI Embeddings API.",
    """
    # Split text into chunks of ~100 tokens (approx.)
    chunk_size = 100
    chunks = [text[i:i+chunk_size] for text in texts for i in range(0, len(text), chunk_size)]
    response = Embedding.create(model=model, input=chunks)
    embeddings = np.array(response['data'][0]['embedding'])
    return embeddings
