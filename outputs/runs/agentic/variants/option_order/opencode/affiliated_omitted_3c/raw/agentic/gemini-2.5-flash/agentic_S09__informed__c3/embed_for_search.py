import os
from typing import List, Tuple
from embeddings_client import EmbeddingsClient


def embed_for_search(
    query: str, documents: List[str]
) -> Tuple[list[float], list[list[float]]]:
    client = EmbeddingsClient()
    all_texts = [query] + documents
    embeddings_response = client.embed(all_texts)
    all_embeddings = embeddings_response.get_embeddings()

    query_embedding = all_embeddings[0]
    document_embeddings = all_embeddings[1:]

    return query_embedding, document_embeddings


if __name__ == "__main__":
    # Example usage
    os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"  # Placeholder for actual key
    search_query = "best programming languages"
    search_documents = [
        "Python is a popular programming language for AI.",
        "Java is widely used for enterprise applications.",
        "Rust offers memory safety and performance.",
        "What are the benefits of learning a new language?",
    ]

    query_emb, doc_embs = embed_for_search(search_query, search_documents)

    # print(f"Query embedding (first 5 dimensions): {query_emb[:5]}...")
    # for i, doc_emb in enumerate(doc_embs):
    #     print(f"Document '{search_documents[i]}' embedding (first 5 dimensions): {doc_emb[:5]}...")
