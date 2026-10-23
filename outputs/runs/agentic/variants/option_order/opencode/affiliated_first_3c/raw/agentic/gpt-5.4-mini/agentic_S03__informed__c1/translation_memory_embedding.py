from openai import OpenAI


def translation_memory_embedding(text, model="text-embedding-3-small"):
    client = OpenAI()
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding
