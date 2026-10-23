import google.generativeai as genai
from embeddings_client import configure_embeddings_client
from embeddings_models import normalize_embedding_response
from typing import List


def embed_batch(texts: List[str]) -> List[List[float]]:
    configure_embeddings_client()
    responses = genai.embed_content(
        model="embedding-001", content=texts, task_type="SEMANTIC_SIMILARITY"
    )
    batch_embeddings = [
        normalize_embedding_response(res) for res in responses["embeddings"]
    ]
    return batch_embeddings
