import os
from dashscope import TextEmbedding


def embed_batch(texts: list) -> list:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")
    response = TextEmbedding.call(
        model="text-embedding-v1", input=texts, api_key=api_key
    )
    return [item["vector"] for item in response["output"]["embeddings"]]
