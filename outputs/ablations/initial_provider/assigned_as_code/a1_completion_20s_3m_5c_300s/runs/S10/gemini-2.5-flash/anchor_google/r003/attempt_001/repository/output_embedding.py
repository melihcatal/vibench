import os
from typing import Any, Dict, List
import google.generativeai as genai
from model_client import GeminiClient
from model_models import EmbeddingResponse

def output_embedding(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = GeminiClient(api_key=config.get("api_key")) # client initialization ensures API key is set
    
    text_to_embed = payload.get("text", "")
    if not text_to_embed:
        raise ValueError("Payload must contain 'text' for embedding.")

    # The embedding model is typically 'embedding-001'
    # We don't need to get it via client.get_model as embed_content is a top-level function or method
    result = genai.embed_content(
        model="models/embedding-001",
        content=text_to_embed,
        task_type="RETRIEVAL_DOCUMENT" # or other appropriate task_type
    )

    # The embedding is usually in result['embedding'] or similar structure depending on the exact response format
    # Assuming the structure is result.embedding
    return {"embedding": result['embedding']}
