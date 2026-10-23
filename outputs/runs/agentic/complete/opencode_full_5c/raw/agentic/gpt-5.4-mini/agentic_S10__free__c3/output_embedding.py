from openai import OpenAI


def output_embedding(text: str):
    client = OpenAI()
    resp = client.embeddings.create(model="text-embedding-3-large", input=text)
    return resp.data[0].embedding
