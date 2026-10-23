import cohere
import os
from typing import List

co = cohere.Client(os.getenv('COHERE_API_KEY'))

def embed_log_messages(messages: List[str]) -> List[List[float]]:
    response = co.embed(
        texts=messages,
        model='embed-english-v3.0',
        input_type='search_query'
    )
    return response.embeddings

def embed_single_log(message: str) -> List[float]:
    return embed_log_messages([message])[0]
