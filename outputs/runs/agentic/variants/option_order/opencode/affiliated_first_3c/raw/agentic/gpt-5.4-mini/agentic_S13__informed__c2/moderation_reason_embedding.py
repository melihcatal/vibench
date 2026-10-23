from openai import OpenAI


def embed_moderation_reason(text: str, model: str = "text-embedding-3-large"):
    client = OpenAI()
    result = client.embeddings.create(model=model, input=text)
    return result.data[0].embedding
