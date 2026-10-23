import speech_client
from typing import List

def embed_text_segments(texts: List[str]) -> List[List[float]]:
    cohere_client = speech_client.get_cohere_client()
    
    response = cohere_client.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="classification"
    )
    return response.embeddings