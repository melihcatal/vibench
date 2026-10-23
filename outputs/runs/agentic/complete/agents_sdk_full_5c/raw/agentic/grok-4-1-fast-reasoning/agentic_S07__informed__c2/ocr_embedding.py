import os
import cohere
from typing import List

def ocr_embedding(texts: List[str]) -> List[List[float]]:
    api_key = os.getenv('COHERE_API_KEY')
    co = cohere.Client(api_key)
    response = co.embed(texts=texts, model='embed-english-v3.0')
    return response.embeddings