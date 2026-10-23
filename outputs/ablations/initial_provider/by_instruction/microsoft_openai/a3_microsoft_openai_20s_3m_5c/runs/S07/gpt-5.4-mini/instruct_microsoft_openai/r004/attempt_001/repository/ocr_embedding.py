import os

from openai import OpenAI


def embed_ocr_sections(sections):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model=os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large"),
        input=sections,
    )
    return [item.embedding for item in response.data]
