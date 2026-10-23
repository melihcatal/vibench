from sentence_transformers import SentenceTransformer
from typing import List


def embed_script(script: str) -> List[float]:
    """Embed narration scripts for voice-asset search using Sentence Transformers."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(script, convert_to_tensor=False)
    return embedding.tolist()