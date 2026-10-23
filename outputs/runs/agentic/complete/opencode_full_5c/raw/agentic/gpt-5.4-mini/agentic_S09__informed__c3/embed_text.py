from embeddings_client import create_client, get_embedding_model
from embeddings_models import EmbeddingRequest


def embed_text(text: str):
    request = EmbeddingRequest(input_text=text)
    client = create_client()
    response = client.embeddings.create(
        model=get_embedding_model(), input=request.input_text
    )
    return response.data[0].embedding
