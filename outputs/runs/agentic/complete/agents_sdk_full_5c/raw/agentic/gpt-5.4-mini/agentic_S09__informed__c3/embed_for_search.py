from embeddings_client import get_client, get_model, normalize_text
from embeddings_models import SearchEmbeddingBundle, normalize_embedding


def embed_for_search(query: str, documents: list[str]) -> SearchEmbeddingBundle:
    client = get_client()
    query_response = client.embed(
        texts=[normalize_text(query)],
        model=get_model(),
        input_type="search_query",
        embedding_types=["float"],
    )
    doc_response = client.embed(
        texts=[normalize_text(document) for document in documents],
        model=get_model(),
        input_type="search_document",
        embedding_types=["float"],
    )
    return SearchEmbeddingBundle(
        query=normalize_embedding(query_response.embeddings.float[0]),
        documents=[normalize_embedding(item) for item in doc_response.embeddings.float],
        query_text=normalize_text(query),
        document_texts=tuple(normalize_text(document) for document in documents),
    )
