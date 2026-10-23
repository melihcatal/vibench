import os
import cohere
from typing import List, Any

def platform_output_embedding(text: str, model: str = "embed-english-v3.0") -> List[float]:
    api_key = os.getenv("COHERE_API_KEY")
    co = cohere.Client(api_key)
    response = co.embed(texts=[text], model=model)
    return response.embeddings[0]
