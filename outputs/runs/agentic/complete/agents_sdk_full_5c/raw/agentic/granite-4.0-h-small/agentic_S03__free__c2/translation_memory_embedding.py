# translation_memory_embedding.py
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def embed_segments(translated_text: str) -> np.ndarray:
    """Embed translated text for similarity search in a translation memory.
    Returns a normalized vector suitable for cosine similarity.
    """
    embeddings = model.encode(translated_text, convert_to_tensor=True)
    return embeddings.numpy()
