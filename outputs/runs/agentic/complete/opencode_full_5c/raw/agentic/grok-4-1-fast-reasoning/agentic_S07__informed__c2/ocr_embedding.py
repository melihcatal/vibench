import os
import openai
from typing import List

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ocr_embedding(sections: List[str]) -> List[List[float]]:
    response = client.embeddings.create(input=sections, model="text-embedding-3-small")
    return [data.embedding for data in response.data]
