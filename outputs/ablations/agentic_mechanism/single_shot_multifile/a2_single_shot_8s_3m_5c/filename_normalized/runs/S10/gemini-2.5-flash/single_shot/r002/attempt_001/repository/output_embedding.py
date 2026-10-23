import os
import openai
from model_client import get_openai_client
from model_models import EmbeddingResult

def get_embedding(text: str, model_name: str = "text-embedding-3-small") -> EmbeddingResult:
    client = get_openai_client()
    
    response = client.embeddings.create(
        input=[text],
        model=model_name
    )
    
    return EmbeddingResult(
        embedding=response.data[0].embedding,
        model_name=model_name
    )
