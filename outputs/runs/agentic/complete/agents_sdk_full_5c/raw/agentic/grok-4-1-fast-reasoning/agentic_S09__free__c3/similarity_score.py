from typing import List
import math
from embeddings_client import get_client
from embeddings_models import MODEL_EMBED, normalize_text

def _cosine_similarity(emb1: List[float], emb2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(emb1, emb2))
    norm1 = math.sqrt(sum(a * a for a in emb1))
    norm2 = math.sqrt(sum(b * b for b in emb2))
    return dot / (norm1 * norm2) if norm1 > 0 and norm2 > 0 else 0.0

def similarity_score(text1: str, text2: str) -> float:
    client = get_client()
    resp1 = client.embeddings.create(model=MODEL_EMBED, input=normalize_text(text1))
    emb1 = resp1.data[0].embedding
    resp2 = client.embeddings.create(model=MODEL_EMBED, input=normalize_text(text2))
    emb2 = resp2.data[0].embedding
    return _cosine_similarity(emb1, emb2)