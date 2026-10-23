from embeddings_client import get_embeddings_client
from typing import List


def generate_text_embedding(text: str) -> List[float]:
    """
    Generates an embedding for a single text string using Gemini API.
    """
    client = get_embeddings_client()
    result = client.embed_content(
        model="models/embedding-001", content=text, task_type="retrieval_document"
    )
    return result["embedding"]
