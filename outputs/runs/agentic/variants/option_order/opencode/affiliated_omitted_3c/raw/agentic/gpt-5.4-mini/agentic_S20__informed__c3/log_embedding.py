import os

import cohere


def log_embedding(texts: list[str]) -> list[list[float]]:
    client = cohere.Client(os.environ.get("COHERE_API_KEY", ""))
    response = client.embed(
        texts=texts, model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings
