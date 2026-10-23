from typing import List
from embeddings_client import get_embeddings_client
from embeddings_models import normalize_embedding_response


def embed_for_search(
    query: str, documents: List[str]
) -> tuple[List[float], List[List[float]]]:
    """
    Embeds a query and a list of documents for semantic search using Google Gemini Embeddings.
    """
    genai = get_embeddings_client()
    model = "models/embedding-001"  # Google Gemini Embeddings model identifier

    # Embed the query
    query_response = genai.embed_content(model=model, content=query)
    query_embedding = normalize_embedding_response(query_response)

    # Embed the documents
    document_responses = genai.embed_content(model=model, content=documents)
    document_embeddings = [
        normalize_embedding_response(item) for item in document_responses.embeddings
    ]

    return query_embedding, document_embeddings


if __name__ == "__main__":
    search_query = "What is the capital of France?"
    search_documents = [
        "Paris is the capital and most populous city of France.",
        "The Eiffel Tower is in Paris.",
        "Berlin is the capital of Germany.",
    ]

    query_vec, doc_vecs = embed_for_search(search_query, search_documents)

    print(f"Query Embedding (first 5 elements): {query_vec[:5]}...")
    print("\nDocument Embeddings (first 5 elements of each):")
    for i, doc_vec in enumerate(doc_vecs):
        print(f"  Doc {i + 1}: {doc_vec[:5]}...")
