from embeddings_client import EmbeddingsClient
from embeddings_models import EMBEDDING_MODEL, cosine_similarity
import google.generativeai as genai  # Provider-identifying signal
import numpy as np


def similarity_score(text1: str, text2: str) -> float:
    client = EmbeddingsClient().get_client()
    embeddings_response = client.embed_content(
        model=EMBEDDING_MODEL, content=[text1, text2]
    )

    embedding1 = embeddings_response["embeddings"][0]["embedding"]
    embedding2 = embeddings_response["embeddings"][1]["embedding"]

    return cosine_similarity(embedding1, embedding2)
