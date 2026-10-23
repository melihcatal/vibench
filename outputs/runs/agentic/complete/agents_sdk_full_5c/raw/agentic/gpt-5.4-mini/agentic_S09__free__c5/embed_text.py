from embeddings_client import OPENAI_EMBEDDING_MODEL, get_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def embed_text(text: str, model: str = OPENAI_EMBEDDING_MODEL) -> EmbeddingResponse:
    client = get_client()
    request = EmbeddingRequest(input_texts=[text], model=model)
    response = client.embeddings.create(model=request.model, input=list(request.input_texts))
    vector = response.data[0].embedding
    return EmbeddingResponse(model=response.model, vectors=[vector])
