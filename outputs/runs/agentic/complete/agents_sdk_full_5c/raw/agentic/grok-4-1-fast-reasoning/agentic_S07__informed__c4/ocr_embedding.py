import os
from openai import OpenAI
from typing import List

def ocr_embedding(sections: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    embeddings = []
    for section in sections:
        response = client.embeddings.create(
            input=section,
            model=model
        )
        embeddings.append(response.data[0].embedding)
    return embeddings
