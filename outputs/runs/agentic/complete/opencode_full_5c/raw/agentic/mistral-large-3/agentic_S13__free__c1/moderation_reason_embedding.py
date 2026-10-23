from typing import Dict, List
from sentence_transformers import SentenceTransformer


def embed_moderation_rationales(rationales: List[str]) -> Dict:
    model = SentenceTransformer("all-MiniLM-L6-v2")

    try:
        embeddings = model.encode(rationales, convert_to_tensor=True)
        return {"embeddings": embeddings.tolist(), "model": "all-MiniLM-L6-v2"}
    except Exception as e:
        return {"error": str(e), "embeddings": []}
