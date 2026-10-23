from typing import List
from embeddings_client import get_openai_client
from embeddings_models import EmbeddingResponse


def generate_embeddings_batch(
    texts: List[str], model: str = "text-embedding-3-small"
) -> List[EmbeddingResponse]:
    """
    Generates embeddings for a batch of texts using OpenAI.
    """
    client = get_openai_client()
    response = client.embeddings.create(input=texts, model=model)

    results = []
    for i, data in enumerate(response.data):
        results.append(EmbeddingResponse(text=texts[i], embedding=data.embedding))

    return results
