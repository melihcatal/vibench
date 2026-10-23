from typing import List
from safety_models import ModerationRationaleEmbedding
from sentence_transformers import SentenceTransformer
import os


def embed_moderation_rationale(rationale: str) -> ModerationRationaleEmbedding:
    """Embed moderation rationales for case retrieval using Cohere Embeddings."""
    import cohere

    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(texts=[rationale], model="embed-english-v3.0")

    return ModerationRationaleEmbedding(
        rationale=rationale, embedding=response.embeddings[0]
    )
