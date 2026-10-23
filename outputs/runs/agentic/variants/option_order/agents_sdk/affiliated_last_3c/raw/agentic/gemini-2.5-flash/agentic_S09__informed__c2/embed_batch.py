import os
import google.generativeai as genai

def embed_batch(texts: list[str]) -> list[list[float]]:
    """
    Generates embeddings for a batch of text strings using Google Gemini Embeddings.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    embeddings = []
    try:
        # For batch embedding, use embed_content which handles multiple items
        # The task_type and title parameters might be needed for specific models/use cases
        # For a generic batch, we can use the default behavior.
        # However, genai.embed_content expects contents to be a list of parts, so for simple strings, 
        # we can just pass the list of strings.
        response = genai.embed_content(
            model="models/embedding-001",
            content=texts,
            task_type="RETRIEVAL_DOCUMENT" # A common task type for batch embedding
        )
        # The response structure is {'embedding': [{'value': [...], 'index': ...}, ...]}
        # We need to extract the 'value' lists.
        for item in response['embeddings']:
            embeddings.append(item)
        return embeddings
    except Exception as e:
        print(f"Error generating batch embeddings: {e}")
        return []

