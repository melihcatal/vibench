import os
import cohere


def embed_script(script: str) -> list[float]:
    api_key = os.getenv("COHERE_API_KEY")
    co = cohere.Client(api_key)
    response = co.embed(texts=[script], model="embed-english-v3.0")
    return response.embeddings[0]
