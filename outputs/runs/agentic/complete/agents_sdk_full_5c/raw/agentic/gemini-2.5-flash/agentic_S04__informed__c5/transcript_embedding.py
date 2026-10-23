import os
import google.generativeai as genai
from typing import List

def get_text_embedding(text: str, model_name: str = "embedding-001") -> List[float]:
    """Generates an embedding for the given text using the Google Gemini Embeddings API."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    result = genai.embed_content(
        model=model_name,
        content=text,
        task_type="RETRIEVAL_DOCUMENT"
    )
    if result and result['embedding']:
        return result['embedding']
    return []
