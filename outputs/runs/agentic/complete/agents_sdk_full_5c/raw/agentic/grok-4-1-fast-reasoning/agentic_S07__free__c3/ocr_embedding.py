from openai import OpenAI
import os
from typing import List

def ocr_embedding(sections: List[str]) -> List[list]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(
        input=sections,
        model="text-embedding-3-small"
    )
    return [embedding.embedding for embedding in response.data]
