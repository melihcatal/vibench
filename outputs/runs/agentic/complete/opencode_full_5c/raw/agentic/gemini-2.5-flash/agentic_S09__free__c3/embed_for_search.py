from embeddings_client import get_cohere_client
from embeddings_models import COHERE_SEARCH_MODEL, extract_embeddings


def embed_for_search(
    query: str, documents: list[str]
) -> tuple[list[float], list[list[float]]]:
    """Embeds a query and documents for semantic search using Cohere."""
    co = get_cohere_client()

    query_embedding_response = co.embed(
        texts=[query], model=COHERE_SEARCH_MODEL, input_type="search_query"
    )
    query_embedding = extract_embeddings(query_embedding_response)[0]

    document_embeddings_response = co.embed(
        texts=documents, model=COHERE_SEARCH_MODEL, input_type="search_document"
    )
    doc_embeddings = extract_embeddings(document_embeddings_response)

    return query_embedding, doc_embeddings
