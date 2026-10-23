import google.generativeai as genai
import os

def embed_for_search(query: str, documents: list[str]) -> tuple[list[float], list[list[float]]]:
    """Embeds a query and a list of documents for semantic search using Google's Generative AI.

    Args:
        query: The search query string.
        documents: A list of document strings to embed.

    Returns:
        A tuple containing:
            - The embedding vector for the query.
            - A list of embedding vectors for the documents.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.get_model("models/embedding-001")

    query_embedding_response = model.embed_content(content=query)
    query_embedding = query_embedding_response["embedding"]

    document_embeddings_response = model.embed_content(content=documents)
    document_embeddings = [item["embedding"] for item in document_embeddings_response["embeddings"]]

    return query_embedding, document_embeddings
