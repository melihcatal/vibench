import os
from openai import OpenAI
from typing import List, Union

def embed_platform_output(text: Union[str, List[str]]) -> List[List[float]]:
    """
    Embed platform outputs using OpenAI Embeddings API.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return [data.embedding for data in response.data]
