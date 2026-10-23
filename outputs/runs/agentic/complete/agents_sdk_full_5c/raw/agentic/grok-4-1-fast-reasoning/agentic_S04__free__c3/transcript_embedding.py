import os
import cohere

def transcript_embedding(segments: list[str]) -> list[list[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is required.")
    co = cohere.Client(api_key)
    response = co.embed(
        texts=segments,
        model="embed-english-v3.0"
    )
    return response.embeddings