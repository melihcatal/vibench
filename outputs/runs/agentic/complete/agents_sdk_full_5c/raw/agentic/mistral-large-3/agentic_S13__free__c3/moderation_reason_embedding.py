from sentence_transformers import SentenceTransformer
from typing import List


def embed_moderation_rationales(rationales: List[str]) -> List[List[float]]:
    """
    Embeds moderation rationales for case retrieval using Sentence Transformers (all-MiniLM-L6-v2).
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(rationales, convert_to_tensor=False)
    return embeddings.tolist()