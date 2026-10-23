import os
import cohere
from typing import List, Any

def embed_output(text: str) -> List[float]:
    api_key = os.getenv("COHERE_API_KEY")
    co = cohere.Client(api_key)
    
    response = co.embed(
        texts=[text],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    
    return response.embeddings[0]