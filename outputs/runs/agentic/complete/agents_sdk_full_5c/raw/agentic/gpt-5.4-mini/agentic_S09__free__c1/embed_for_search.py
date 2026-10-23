from embeddings_client import get_openai_embeddings_client
from embeddings_models import EmbeddingRequest, normalize_embedding_response


OPENAI_MODEL = "text-embedding-3-small"


def embed_for_search(query: str, documents):
    client = get_openai_embeddings_client()
    texts = [query, *list(documents)]
    request = EmbeddingRequest(texts=texts, model=OPENAI_MODEL)
    response = client.embeddings.create(model=request.model, input=request.texts)
    normalized = normalize_embedding_response(response)
    return {"query_embedding": normalized.embeddings[0], "document_embeddings": normalized.embeddings[1:]}
