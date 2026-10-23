import os
import cohere
from typing import List

def ocr_embedding(texts: List[str]) -> List[List[float]]:
    """
    Embed extracted document sections for semantic retrieval using Cohere Embed API.
    """
    api_key = os.getenv('COHERE_API_KEY')
    co = cohere.Client(api_key)
    
    response = co.embed(
        texts=texts,
        model='embed-english-v3.0',
        input_type='search_document'
    )
    
    return response.embeddings
