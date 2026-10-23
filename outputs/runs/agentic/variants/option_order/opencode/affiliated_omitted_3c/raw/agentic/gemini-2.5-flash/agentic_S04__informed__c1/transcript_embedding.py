import os
import cohere


def embed_transcript_segments(segments: list[str]) -> list[list[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set")

    co = cohere.Client(api_key)

    response = co.embed(
        texts=segments,
        model="embed-english-v3.0",  # Using a common Cohere embedding model
        input_type="search_document",
    )
    return response.embeddings
