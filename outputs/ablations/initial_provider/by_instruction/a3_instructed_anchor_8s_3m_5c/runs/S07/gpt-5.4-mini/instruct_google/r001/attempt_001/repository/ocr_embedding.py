import os

import openai


def embed_document_sections(sections: list[str]) -> list[list[float]]:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Embedding.create(model="text-embedding-3-small", input=sections)
    return [item["embedding"] for item in response["data"]]
