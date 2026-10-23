from openai import OpenAI


def embed_document_sections(sections: list[str]) -> list[list[float]]:
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-large", input=sections)
    return [item.embedding for item in response.data]
