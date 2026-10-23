import os
import cohere
from typing import List

def translation_memory_embedding(segment: str) -> List[float]:
    \"\"\"
    Embed translated segments for translation-memory search using Cohere.
    \"\"\"
    api_key = os.getenv('COHERE_API_KEY')
    if not api_key:
        raise ValueError('COHERE_API_KEY environment variable is required.')
    client = cohere.Client(api_key)
    response = client.embed(
        texts=[segment],
        model='embed-english-v3.0',
        input_type='search_query'
    )
    return response.embeddings[0]