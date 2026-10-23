import os
import voyageai
from typing import List
from model_client import VOYAGE_API_KEY

def embed_output(text_to_embed: str) -> List[float]:
    """
    Embeds model outputs using the Voyage AI API for clustering or retrieval.
    """
    if not VOYAGE_API_KEY:
        raise ValueError("VOYAGE_API_KEY environment variable not set.")

    vo = voyageai.Client(api_key=VOYAGE_API_KEY)

    # The Voyage API can take a list of texts, here we embed one.
    result = vo.embed([text_to_embed], model="voyage-2", input_type="document")
    
    return result.embeddings[0]
