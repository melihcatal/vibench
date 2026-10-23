import os
import google.generativeai as genai
from typing import List

def embed_moderation_rationales(rationales: List[str]):
    """
    Embed moderation rationales for case retrieval using Gemini Embeddings.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)

    # The embedding model to use
    embedding_model = "models/embedding-001"

    try:
        response = genai.embed_content(
            model=embedding_model,
            content=rationales
        )
        # The embedding response structure can vary, typically embeddings are in a list
        return response['embedding']
    except Exception as e:
        print(f"Error generating embeddings with Gemini API: {e}")
        return None
