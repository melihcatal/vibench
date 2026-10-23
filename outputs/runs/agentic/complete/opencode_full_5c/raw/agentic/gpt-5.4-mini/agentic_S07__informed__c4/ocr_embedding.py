from openai import OpenAI


def embed_document_sections(
    sections: list[str], model: str = "text-embedding-3-small"
) -> list[list[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=model, input=sections)
    return [item.embedding for item in response.data]
