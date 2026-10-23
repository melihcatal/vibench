from openai import OpenAI


def log_embedding(messages):
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small", input=list(messages)
    )
    return [item.embedding for item in response.data]
