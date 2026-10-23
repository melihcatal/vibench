import os
import cohere
from typing import List


def generate_log_embeddings(log_messages: List[str]) -> List[List[float]]:
    api_key = os.getenv("COHERE_API_KEY")
    co = cohere.Client(api_key)
    response = co.embed(
        texts=log_messages, model="embed-english-v3.0", input_type="search_document"
    )
    return response.embeddings
