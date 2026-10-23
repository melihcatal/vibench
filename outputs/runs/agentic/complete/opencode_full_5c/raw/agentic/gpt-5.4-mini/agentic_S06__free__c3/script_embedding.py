from openai import OpenAI


def embed_script(script: str) -> list[float]:
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-small", input=script)
    return response.data[0].embedding
