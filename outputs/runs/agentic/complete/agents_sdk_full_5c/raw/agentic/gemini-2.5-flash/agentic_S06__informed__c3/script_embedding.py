import os
import google.generativeai as genai
from typing import List

def get_text_embedding_gemini(text_content: str, api_key: str, model_name: str = "models/embedding-001") -> List[float]:
    """
    Generates an embedding for the given text content using Google Gemini Embeddings.

    Args:
        text_content: The text to embed.
        api_key: Your Google API key for Gemini.
        model_name: The name of the embedding model (default: 'models/embedding-001').

    Returns:
        A list of floats representing the embedding vector.
    """
    genai.configure(api_key=api_key)

    # It's recommended to embed content in batches for production, but for a single script embedding,
    # this direct call is fine.
    try:
        response = genai.embed_content(
            model=model_name,
            content=text_content,
            task_type="RETRIEVAL_DOCUMENT" # or "RETRIEVAL_QUERY", "SEMANTIC_SIMILARITY", etc.
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding with Gemini: {e}")
        return []

