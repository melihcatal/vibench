from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response
import numpy as np


def similarity_score(payload, config=None):
    client = get_embeddings_client(config)
    embedding1 = client.models.embed_content(model="gemini-embedding-001", contents=payload["text1"])[0]
    embedding2 = client.models.embed_content(model="gemini-embedding-001", contents=payload["text2"])[0]
    normalized_embedding1 = normalize_embedding_response(embedding1)
    normalized_embedding2 = normalize_embedding_response(embedding2)
    cosine_similarity = np.dot(normalized_embedding1, normalized_embedding2) / (np.linalg.norm(normalized_embedding1) * np.linalg.norm(normalized_embedding2))
    return {"similarity_score": cosine_similarity}