import os
from typing import List, Optional
import cohere


def generate_output_embedding(
    text: str,
    model: Optional[str] = "embed-english-v3.0"
) -> List[float]:
    """
    Embed model outputs for clustering or retrieval using Cohere's embeddings API.
    """
    co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
    
    response = co.embed(
        texts=[text],
        model=model,
        input_type="search_document"
    )
    
    return response.embeddings[0]