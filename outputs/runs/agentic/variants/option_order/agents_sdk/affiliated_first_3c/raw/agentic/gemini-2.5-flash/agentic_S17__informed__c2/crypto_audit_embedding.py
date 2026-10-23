import os
import google.generativeai as genai

def embed_audit_notes(audit_notes: list[str]) -> list[list[float]]:
    """
    Embeds crypto audit notes for semantic search using the Gemini Embeddings API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)

    model = "models/embedding-001" # Concrete model identifier for Gemini Embeddings

    embeddings = []
    for note in audit_notes:
        response = genai.embed_content(
            model=model,
            content=note,
            task_type="RETRIEVAL_DOCUMENT" # Specify task type for better embeddings
        )
        embeddings.append(response['embedding'])
    
    return embeddings

def embed_query(query_text: str) -> list[float]:
    """
    Embeds a single query text for semantic search against audit notes.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)

    model = "models/embedding-001"

    response = genai.embed_content(
        model=model,
        content=query_text,
        task_type="RETRIEVAL_QUERY" # Specify task type for better embeddings
    )
    return response['embedding']
