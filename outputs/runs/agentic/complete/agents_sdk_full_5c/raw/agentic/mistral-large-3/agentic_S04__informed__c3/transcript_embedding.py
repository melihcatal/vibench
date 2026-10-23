import os
from typing import List, Dict
import cohere

def embed_transcript_segments(segments: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Embeds transcript segments using Cohere Embed API.
    Returns segments with their embeddings.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    
    co = cohere.Client(api_key)
    
    texts = [segment["text"] for segment in segments]
    response = co.embed(
        texts=texts,
        model="embed-english-v3.0"
    )
    
    return [
        {
            **segment,
            "embedding": embedding
        }
        for segment, embedding in zip(segments, response.embeddings)
    ]