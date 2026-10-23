import os
from dashscope import TextEmbedding


def get_embeddings_client():
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")
    return TextEmbedding(api_key=api_key)
