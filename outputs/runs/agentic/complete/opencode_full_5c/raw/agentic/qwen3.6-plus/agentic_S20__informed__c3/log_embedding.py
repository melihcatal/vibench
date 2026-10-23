import os

from openai import OpenAI

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def embed_log_messages(messages: list[str]) -> list[dict]:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=messages,
    )
    embeddings = []
    for item in response.data:
        embeddings.append(
            {
                "text": messages[item.index],
                "embedding": item.embedding,
                "model": response.model,
                "index": item.index,
            }
        )
    return embeddings


def embed_single_log_message(text: str) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.embeddings.create(
        model=OPENAI_EMBEDDING_MODEL,
        input=[text],
    )
    item = response.data[0]
    return {
        "text": text,
        "embedding": item.embedding,
        "model": response.model,
        "index": item.index,
    }


if __name__ == "__main__":
    sample_messages = [
        "Database connection pool exhausted",
        "Request timeout after 30 seconds",
        "Circuit breaker opened for downstream service",
    ]
    results = embed_log_messages(sample_messages)
    for r in results:
        print(f"index={r['index']} model={r['model']} dim={len(r['embedding'])}")
