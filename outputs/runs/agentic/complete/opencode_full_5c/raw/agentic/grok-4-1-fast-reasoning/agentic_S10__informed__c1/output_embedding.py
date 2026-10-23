import os
import cohere


def embed_output(text: str) -> list[float]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY not set")
    co = cohere.Client(api_key=api_key)
    response = co.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_query"
    )
    return response.embeddings[0]
