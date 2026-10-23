from openai import OpenAI
import os
from typing import List, Union

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translation_memory_embedding(text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
    """
    Embed translated segments for translation-memory search using OpenAI Embeddings.
    """
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    if isinstance(text, str):
        return response.data[0].embedding
    return [data.embedding for data in response.data]