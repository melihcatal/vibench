from openai import OpenAI

from document_client import load_config


def ocr_embedding(sections: list[str]) -> list[list[float]]:
    client = OpenAI(api_key=load_config().api_key)
    result = client.embeddings.create(model="text-embedding-3-small", input=sections)
    return [item.embedding for item in result.data]
