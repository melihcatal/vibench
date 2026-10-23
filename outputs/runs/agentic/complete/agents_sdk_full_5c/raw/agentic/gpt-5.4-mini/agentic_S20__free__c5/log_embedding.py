from __future__ import annotations

from openai import OpenAI

from observability_client import build_openai_client
from observability_models import EmbeddingRequest


def embed_log_messages(client: OpenAI, request: EmbeddingRequest):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=request.messages,
    )
    return [item.embedding for item in response.data]


def main() -> None:
    client = build_openai_client()
    request = EmbeddingRequest(messages=["Checkout completed successfully", "Payment authorization failed"])
    embed_log_messages(client, request)


if __name__ == "__main__":
    main()
