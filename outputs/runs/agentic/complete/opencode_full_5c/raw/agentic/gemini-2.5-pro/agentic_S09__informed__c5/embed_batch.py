from embeddings_client import get_embeddings_client
from typing import List


def generate_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a batch of text strings using Gemini API.
    """
    client = get_embeddings_client()
    result = client.embed_content(
        model="models/embedding-001", content=texts, task_type="retrieval_document"
    )
    return [embedding for embedding in result["embedding"]]
