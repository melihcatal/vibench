from speech_client import get_cohere_client
from speech_models import EmbeddingRequest


def embed_script(request: EmbeddingRequest) -> dict:
    client = get_cohere_client()
    response = client.embed(
        texts=request.texts,
        model="embed-english-v3.0",
        input_type="search_document",
    )
    return response.embeddings
