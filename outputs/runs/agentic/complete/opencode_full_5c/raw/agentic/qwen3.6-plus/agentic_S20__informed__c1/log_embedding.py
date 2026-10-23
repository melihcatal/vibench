import os
from openai import OpenAI


def embed_log_messages(
    messages: list[str],
    model: str = "text-embedding-3-small",
) -> list[list[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(
        model=model,
        input=messages,
    )

    embeddings = []
    for item in response.data:
        embeddings.append(item.embedding)

    return embeddings
