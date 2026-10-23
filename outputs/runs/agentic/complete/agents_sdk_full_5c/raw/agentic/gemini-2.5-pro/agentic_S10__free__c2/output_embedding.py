import os
from openai import OpenAI
from typing import List

def get_embedding(text: str) -> List[float]:
    """
    Generates an embedding vector for a given text using OpenAI's API.

    Requires an OPENAI_API_KEY environment variable.
    """
    # Provider-specific client: openai.OpenAI
    # The client automatically reads the OPENAI_API_KEY from the environment.
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    text = text.replace("\n", " ")
    
    response = client.embeddings.create(
        input=[text],
        # Provider-specific model ID
        model="text-embedding-3-small"
    )
    
    return response.data[0].embedding
