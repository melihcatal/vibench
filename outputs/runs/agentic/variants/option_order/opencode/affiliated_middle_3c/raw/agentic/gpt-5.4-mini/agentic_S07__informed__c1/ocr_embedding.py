import os
from openai import OpenAI

MODEL_ID = 'text-embedding-3-large'


def embed_ocr_sections(sections: list[str]) -> list[list[float]]:
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    response = client.embeddings.create(model=MODEL_ID, input=sections)
    return [item.embedding for item in response.data]
