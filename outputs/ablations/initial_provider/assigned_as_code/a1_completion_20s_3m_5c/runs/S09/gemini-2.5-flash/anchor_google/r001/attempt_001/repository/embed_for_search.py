from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingForSearchRequest, EmbeddingResponse

def embed_for_search(payload: dict, config: dict = None) -> dict:
    config = config or {}
    client = EmbeddingsClient(api_key=config.get("api_key"))

    query_texts = payload.get("query_texts")
    document_texts = payload.get("document_texts")

    if not query_texts or not document_texts:
        raise ValueError("Payload must contain 'query_texts' and 'document_texts'.")

    request = EmbeddingForSearchRequest(
        query_texts=query_texts,
        document_texts=document_texts,
        model=payload.get("model", "gemini-embedding-001")
    )

    query_embeddings = client.embed_content(
        model=request.model,
        texts=request.to_client_query_payload()
    )

    document_embeddings = client.embed_content(
        model=request.model,
        texts=request.to_client_document_payload()
    )

    return {
        "query_embeddings": EmbeddingResponse.from_client_response(query_embeddings).to_dict()["embeddings"],
        "document_embeddings": EmbeddingResponse.from_client_response(document_embeddings).to_dict()["embeddings"]
    }
