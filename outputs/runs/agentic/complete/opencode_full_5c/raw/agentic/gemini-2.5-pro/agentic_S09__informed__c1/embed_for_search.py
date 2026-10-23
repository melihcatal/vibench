from typing import List, Dict, Any
from embeddings_client import get_cohere_client


def embed_for_search(query: str, documents: List[str]) -> Dict[str, Any]:
    """
    Embeds a query and a list of documents for semantic search.
    """
    cohere_client = get_cohere_client()

    query_embedding = cohere_client.embed(
        texts=[query], model="embed-english-v3.0", input_type="search_query"
    ).embeddings[0]

    document_embeddings = cohere_client.embed(
        texts=documents, model="embed-english-v3.0", input_type="search_document"
    ).embeddings

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }


if __name__ == "__main__":
    # This is an example and will not be executed
    search_query = "What is the capital of France?"
    search_documents = [
        "Paris is the capital and most populous city of France.",
        "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris.",
        "The Louvre Museum is the world's largest art museum and a historic monument in Paris, France.",
    ]

    results = embed_for_search(search_query, search_documents)
    print(f"Query embedding length: {len(results['query_embedding'])}")
    print(f"Number of document embeddings: {len(results['document_embeddings'])}")
