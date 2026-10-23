import os
from dashscope import TextEmbedding


def embed_text(text: str) -> list:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")
    response = TextEmbedding.call(model="text-embedding-v1", input=text)
    if response.status_code == 200:
        return response.output.embedding
    else:
        raise Exception(f"Failed to get embedding: {response.status_code}")
