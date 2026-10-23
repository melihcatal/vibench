import os
from typing import List
import voyageai

def embed_transcript_segments(segments: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of transcript segments using Voyage AI.

    Args:
        segments: A list of text strings (e.g., sentences or paragraphs).

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    api_key = os.getenv("VOYAGE_API_KEY")
    if not api_key:
        raise ValueError("VOYAGE_API_KEY environment variable not set.")

    vo = voyageai.Client(api_key=api_key)

    result = vo.embed(
        texts=segments, 
        model="voyage-2",
        input_type="document"
    )
    
    return result.embeddings
