import os
import google.generativeai as genai

def embed_query(query: str) -> list[float]:
    """Embeds a query for semantic search using Google Gemini Embeddings."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"
    response = genai.embed_content(
        model=model,
        content=query,
        task_type="RETRIEVAL_QUERY"
    )
    return response["embedding"]

def embed_documents(documents: list[str]) -> list[list[float]]:
    """Embeds a list of documents for semantic search using Google Gemini Embeddings."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = "models/embedding-001"
    response = genai.embed_content(
        model=model,
        content=documents,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return [item["embedding"] for item in response["embeddings"]]

