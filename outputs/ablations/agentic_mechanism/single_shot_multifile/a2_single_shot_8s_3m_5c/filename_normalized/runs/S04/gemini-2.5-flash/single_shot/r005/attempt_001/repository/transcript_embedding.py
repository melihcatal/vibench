import os
from typing import List, Dict
import openai

# OpenAI Configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def embed_text_segments(text_segments: List[str], model_name: str = "text-embedding-ada-002") -> List[List[float]]:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    openai.api_key = OPENAI_API_KEY

    # The OpenAI API can take a list of texts for embedding in a single call
    response = openai.embeddings.create(
        input=text_segments,
        model=model_name
    )
    return [data.embedding for data in response.data]