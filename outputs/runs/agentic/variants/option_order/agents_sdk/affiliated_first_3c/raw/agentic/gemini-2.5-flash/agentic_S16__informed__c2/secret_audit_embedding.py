import os
import google.generativeai as genai
import typing

def embed_audit_note(audit_note: str) -> typing.List[float]:
    """Embeds secret audit notes for semantic search using Google Gemini Embeddings.
    
    Args:
        audit_note: The audit note text to embed.
        
    Returns:
        A list of floats representing the embedding vector.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=google_api_key)

    # Use a specific embedding model, e.g., 'embedding-001'
    model_name = "models/embedding-001"

    result = genai.embed_content(
        model=model_name,
        content=audit_note,
        task_type="RETRIEVAL_DOCUMENT")
    
    return result['embedding']

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_API_KEY environment variable
    # note = "Accessed production database secret for emergency debugging on 2023-10-27."
    # embedding = embed_audit_note(note)
    # print(f"Embedding for audit note (first 5 values): {embedding[:5]}")
    # print(f"Embedding dimension: {len(embedding)}")
    pass
