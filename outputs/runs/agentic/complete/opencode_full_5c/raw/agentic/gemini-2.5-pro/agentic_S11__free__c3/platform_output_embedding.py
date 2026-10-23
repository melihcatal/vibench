from model_client import get_cohere_client
from model_models import EmbeddingResponse


def get_text_embedding(text: str) -> EmbeddingResponse:
    cohere_client = get_cohere_client()

    response = cohere_client.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )

    return EmbeddingResponse(embedding=response.embeddings[0])
