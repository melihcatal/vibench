import os
from typing import List, Union
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_script(script: str) -> List[float]:
    """
    Embed narration script using OpenAI text-embedding-3-small.
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=script
    )
    return response.data[0].embedding

def embed_scripts(scripts: Union[str, List[str]]) -> List[List[float]]:
    """
    Batch embed narration scripts.
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=scripts
    )
    return [item.embedding for item in response.data]
