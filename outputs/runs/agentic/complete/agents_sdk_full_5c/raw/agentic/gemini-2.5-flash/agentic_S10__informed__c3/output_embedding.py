import os
import google.generativeai as genai
from model_client import get_gemini_embedder
from typing import List

def embed_output(text: str) -> List[float]:
    """
    Embeds model outputs for clustering or retrieval using Google Gemini Embeddings.
    """
    # Using 'models/embedding-001' as the concrete model identifier
    # The client is configured via GOOGLE_API_KEY in model_client.py
    embedding_model = get_gemini_embedder("models/embedding-001")
    response = genai.embed_content(
        model=embedding_model,
        content=text,
        task_type="RETRIEVAL_DOCUMENT" # Specify task type if applicable
    )
    return response['embedding'][0]
