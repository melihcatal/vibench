import cohere
import os

co = cohere.Client(os.getenv('COHERE_API_KEY'))

def embed_log_message(text: str) -> list[float]:
    response = co.embed(
        texts=[text],
        model='embed-english-v3.0',
        input_type='search_query'
    )
    return response.embeddings[0]
