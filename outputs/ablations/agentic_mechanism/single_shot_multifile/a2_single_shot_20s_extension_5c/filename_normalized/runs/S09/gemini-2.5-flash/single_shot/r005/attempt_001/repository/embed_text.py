import os
import openai
from typing import List

def get_single_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    client = openai.OpenAI(api_key=api_key)
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding
