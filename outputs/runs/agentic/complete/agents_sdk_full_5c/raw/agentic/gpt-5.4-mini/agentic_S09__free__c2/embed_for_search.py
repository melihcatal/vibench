from embeddings_client import get_openai_client
from embeddings_models import EmbeddingRequest, normalize_embedding_response

OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def embed_for_search(query: str, documents: list[str]) -> dict[str, list[list[float]] | list[float]]:
    client = get_openai_client()
    query_resp = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=query)
    doc_req = EmbeddingRequest(texts=documents, model=OPENAI_EMBEDDING_MODEL)
    doc_resp = client.embeddings.create(model=doc_req.model, input=doc_req.texts)
    return {
        "query_embedding": normalize_embedding_response(query_resp)[0],
        "document_embeddings": normalize_embedding_response(doc_resp),
    }
