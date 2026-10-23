import os
import cohere
from typing import List

def embed_output(texts: List[str], model_id: str = "embed-english-v3.0") -> List[List[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=texts,
            model=model_id,
            input_type="search_document"
        )
        return response.embeddings
    except Exception as e:
        print(f"Error generating embeddings with Cohere: {e}")
        return []
