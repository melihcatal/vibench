import os
from typing import List, Dict
import google.generativeai as genai

from embeddings_client import get_gemini_embedding_model
from embeddings_models import EmbeddingRequest, EmbeddingResponse

def embed_batch(texts: List[str], api_key: str = None) -> Dict[str, List[List[float]]]:
    """Generates embeddings for a batch of texts using Google's Gemini embedding model."""
    model = get_gemini_embedding_model(api_key)
    
    # The genai.embed_content function takes a list of strings directly for batch processing
    response = genai.embed_content(model=model, content=texts, task_type="SEMANTIC_SIMILARITY")
    
    embedding_response = EmbeddingResponse.from_genai_response(response, model="models/embedding-001")
    return {"embeddings": embedding_response.embeddings}
