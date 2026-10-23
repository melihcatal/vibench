from openai import OpenAI
from typing import List
from document_client import Config


def ocr_embedding(sections: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    response = client.embeddings.create(input=sections, model="text-embedding-3-small")
    return [item.embedding for item in response.data]
