import os
from openai import OpenAI
from typing import List

def get_output_embedding(text: str) -> List[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small",
    )
    return response.data[0].embedding
