import os
import cohere
from typing import List

def create_translation_embedding(text_segment: str) -> List[float]:
    """
    Creates an embedding for a translated text segment for similarity search.
    Provider: Cohere
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    # Provider-specific client class from the Cohere SDK
    co = cohere.Client(api_key)

    # Provider-specific model identifier
    response = co.embed(
        texts=[text_segment],
        model='embed-english-v3.0',
        input_type='search_document'
    )
    
    # The response contains a list of embeddings, one for each input text.
    return response.embeddings[0]
