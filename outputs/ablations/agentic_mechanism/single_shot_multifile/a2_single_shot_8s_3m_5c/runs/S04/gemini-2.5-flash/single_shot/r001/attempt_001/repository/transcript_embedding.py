import os
from typing import List, Dict, Any
import openai

def get_embeddings(text_segments: List[str]) -> List[List[float]]:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    # Using a concrete model identifier for OpenAI Embeddings
    model_id = "text-embedding-ada-002" # or "text-embedding-3-small" / "text-embedding-3-large"

    response = openai.embeddings.create(input=text_segments, model=model_id)
    
    embeddings = [data.embedding for data in response.data]
    return embeddings