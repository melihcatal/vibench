from openai import OpenAI

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def log_embedding(text: str) -> list[float]:
    client = OpenAI()
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    return list(response.data[0].embedding)
