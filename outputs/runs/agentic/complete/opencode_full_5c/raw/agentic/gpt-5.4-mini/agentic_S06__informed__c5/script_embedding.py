from openai import OpenAI


def embed_script(text: str):
    client = OpenAI()
    result = client.embeddings.create(model="text-embedding-3-large", input=text)
    return result.data[0].embedding
