import os

from openai import OpenAI


def embed_ocr_sections(sections):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(model="text-embedding-3-small", input=sections)
    return [item.embedding for item in response.data]
