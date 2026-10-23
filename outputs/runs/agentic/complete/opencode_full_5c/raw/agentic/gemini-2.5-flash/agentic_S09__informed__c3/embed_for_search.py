import os
import google.generativeai as genai


def embed_for_search(
    query: str, documents: list[str]
) -> tuple[list[float], list[list[float]]]:
    """
    Generates embedding vectors for a query and a list of documents for semantic search.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"

    query_embedding_response = genai.embed_content(
        model=model, content=query, task_type="RETRIEVAL_QUERY"
    )
    query_embedding = query_embedding_response["embedding"]

    document_embeddings_response = genai.embed_content(
        model=model, content=documents, task_type="RETRIEVAL_DOCUMENT"
    )
    document_embeddings = [
        emb["embedding"] for emb in document_embeddings_response["embeddings"]
    ]

    return query_embedding, document_embeddings
