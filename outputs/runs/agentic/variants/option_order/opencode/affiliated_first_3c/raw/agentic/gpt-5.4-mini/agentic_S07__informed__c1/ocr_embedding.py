from openai import OpenAI


def embed_sections(sections):
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-small", input=sections)
    return [item.embedding for item in response.data]
