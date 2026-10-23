import os
import cohere
from typing import List

COHERE_API_KEY = os.getenv('COHERE_API_KEY')

def embed_output(text: str) -> List[float]:
    \"\"\"Embed model outputs for clustering or retrieval using Cohere.\"\"
    co = cohere.Client(COHERE_API_KEY)
    response = co.embed(
        texts=[text],
        model='embed-english-v3.0',
        input_type='search_query'
    )
    return response.embeddings[0]
