import os
import cohere


def embed_output(text: str) -> list[float]:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise RuntimeError("COHERE_API_KEY is required")
    client = cohere.Client(api_key)
    result = client.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_document"
    )
    return result.embeddings[0]
