import os
import cohere
from typing import List

def platform_output_embedding(text: str) -> List[float]:
    api_key = os.getenv('COHERE_API_KEY')
    co = cohere.Client(api_key)
    response = co.embed(
        texts=[text],
        model='embed-english-v3.0',
        input_type='search_query'
    )
    return response.embeddings[0]
