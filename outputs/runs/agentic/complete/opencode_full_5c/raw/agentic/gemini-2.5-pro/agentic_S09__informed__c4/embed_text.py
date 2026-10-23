from embeddings_client import get_openai_client
from embeddings_models import EmbeddingResponse


def generate_embedding(
    text: str, model: str = "text-embedding-3-small"
) -> EmbeddingResponse:
    """
    Generates an embedding vector for a single text string using OpenAI.
    """
    client = get_openai_client()
    response = client.embeddings.create(input=[text], model=model)
    embedding_vector = response.data[0].embedding
    return EmbeddingResponse(text=text, embedding=embedding_vector)
