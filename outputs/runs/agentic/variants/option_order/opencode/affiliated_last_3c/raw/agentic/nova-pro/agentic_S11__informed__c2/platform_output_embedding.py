import os
from dashscope import Embedding


def embed_text(text):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable is not set")

    model = Embedding(model="text-embedding-v1")
    response = model.call(api_key=api_key, text=text)
    return response.outputs[0].embedding
