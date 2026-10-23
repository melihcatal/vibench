import os
from typing import List, Dict
import cohere

def embed_transcript_segments(segments: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Embeds transcript segments for semantic retrieval using Cohere's embeddings API.
    Returns segments with their embeddings.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    
    co = cohere.Client(api_key)
    
    texts = [segment["text"] for segment in segments]
    response = co.embed(texts=texts, model="large")
    
    return [{
        **segments[i],
        "embedding": response.embeddings[i]
    } for i in range(len(segments))]