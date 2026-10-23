from model_client import LLMClient
from model_models import EmbeddingRequest, EmbeddingResponse
from typing import List

def embed_output(text: str) -> EmbeddingResponse:
    """Embed model outputs for clustering or retrieval using Gemini Embeddings."""
    llm_client = LLMClient().get_client()
    model = llm_client.GenerativeModel('embedding-001')

    result = model.embed_content(model=model, content=text)
    return EmbeddingResponse(embedding=result['embedding'], raw_response=result)
