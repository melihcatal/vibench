from openai import OpenAI


def embed_script(text: str, model: str = 'text-embedding-3-large') -> list[float]:
    client = OpenAI()
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding
