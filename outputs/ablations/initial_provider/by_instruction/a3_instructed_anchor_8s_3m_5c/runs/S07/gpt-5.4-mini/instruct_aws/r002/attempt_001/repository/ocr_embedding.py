from openai import OpenAI


def embed_document_sections(sections: list[str]) -> dict:
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-large", input=sections)
    return response.model_dump()
