import os
from openai import OpenAI
from typing import List


def embed_log_messages(log_messages: List[str]) -> List[list[float]]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small", input=log_messages
    )
    return [item.embedding for item in response.data]


if __name__ == "__main__":
    sample_logs = [
        "Database connection timeout error",
        "User authentication succeeded",
        "Payment gateway unavailable",
    ]
    embeddings = embed_log_messages(sample_logs)
    print(
        f"Generated {len(embeddings)} embeddings, each of dimension {len(embeddings[0]) if embeddings else 0}"
    )
