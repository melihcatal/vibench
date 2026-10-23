import cohere
import os
from typing import List, Any

def embed_platform_output(
    output_text: str
) -> List[float]:
    client = cohere.Client(api_key=os.getenv('COHERE_API_KEY'))
    response = client.embed(
        texts=[output_text],
        model='embed-english-v3.0',
        input_type='search_document'
    )
    return response.embeddings[0]