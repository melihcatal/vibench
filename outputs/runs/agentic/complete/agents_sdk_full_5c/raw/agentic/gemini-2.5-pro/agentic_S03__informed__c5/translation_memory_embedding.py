import os
import cohere
from typing import List

def embed_translated_segment(text: str) -> List[float]:
    """
    Embeds a translated text segment for translation-memory search
    using the Cohere Embed API.
    
    Expects COHERE_API_KEY environment variable.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
        
    co = cohere.Client(api_key)
    
    response = co.embed(
        texts=[text],
        model='embed-english-v3.0',
        input_type='search_document'
    )
    
    return response.embeddings[0]

def embed_translated_segments_batch(texts: List[str]) -> List[List[float]]:
    """
    Embeds a batch of translated text segments using Cohere.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=texts,
        model='embed-english-v3.0',
        input_type='search_document'
    )

    return response.embeddings
