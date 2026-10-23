from openai import OpenAI


def moderation_reason_embedding(reason_text: str):
    client = OpenAI()
    return client.embeddings.create(
        model="text-embedding-3-small",
        input=reason_text,
    )
