from openai import OpenAI


def embed_script(text: str, model: str = "text-embedding-3-large"):
    client = OpenAI()
    return client.embeddings.create(model=model, input=text).data[0].embedding
