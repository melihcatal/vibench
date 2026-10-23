import voyageai
from model_client import VOYAGE_API_KEY
from typing import List

def embed_text_voyage(text: str) -> List[float]:
    """
    Generates embeddings for a given text using Voyage AI.
    """
    if not VOYAGE_API_KEY:
        raise ValueError("VOYAGE_API_KEY environment variable not set.")

    # Provider-specific client class: voyageai.Client
    vo = voyageai.Client(api_key=VOYAGE_API_KEY)

    # Provider-specific model ID: voyage-large-2
    result = vo.embed(
        [text],
        model="voyage-large-2",
        input_type="document"
    )

    return result.embeddings[0]
