from openai import OpenAI

MODEL = "text-embedding-3-small"


def moderation_reason_embedding(rationale: str):
    client = OpenAI()
    response = client.embeddings.create(model=MODEL, input=rationale)
    return response.data[0].embedding
