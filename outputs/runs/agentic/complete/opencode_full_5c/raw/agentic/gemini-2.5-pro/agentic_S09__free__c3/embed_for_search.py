from typing import List, Dict, Any
from embeddings_client import get_embeddings_client


def generate_search_embeddings(query: str, documents: List[str]) -> Dict[str, Any]:
    """
    Generates embeddings for a query and a list of documents for semantic search.
    """
    client = get_embeddings_client()

    query_embedding_result = client.get_embeddings([query], task_type="RETRIEVAL_QUERY")
    query_embedding = query_embedding_result[0].values

    document_embeddings_result = client.get_embeddings(
        documents, task_type="RETRIEVAL_DOCUMENT"
    )
    document_embeddings = [e.values for e in document_embeddings_result]

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }


if __name__ == "__main__":
    query_text = "What is the capital of France?"
    document_texts = [
        "Paris is the capital and most populous city of France.",
        "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris.",
        "France is a country in Western Europe.",
    ]

    search_embeddings = generate_search_embeddings(query_text, document_texts)

    print("Query Embedding:", search_embeddings["query_embedding"][:5])
    print("Document Embeddings:")
    for i, doc_emb in enumerate(search_embeddings["document_embeddings"]):
        print(f"  Document {i + 1}:", doc_emb[:5])
