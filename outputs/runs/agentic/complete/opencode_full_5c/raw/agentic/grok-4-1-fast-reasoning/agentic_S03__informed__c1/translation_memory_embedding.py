import os
import cohere


def translation_memory_embedding(text: str) -> list[float]:
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(
        texts=[text], model="embed-english-v3.0", input_type="search_query"
    )
    return response.embeddings[0]
