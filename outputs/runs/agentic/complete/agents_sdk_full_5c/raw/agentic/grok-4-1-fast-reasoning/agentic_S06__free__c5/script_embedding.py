import os
from typing import List
from openai import OpenAI

def embed_script(script: str) -> List[float]:
    """
    Embeds narration script for voice-asset search using OpenAI embeddings.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('OPENAI_API_KEY environment variable not set')
    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        input=script,
        model='text-embedding-3-small'
    )
    return [float(x) for x in response.data[0].embedding]
