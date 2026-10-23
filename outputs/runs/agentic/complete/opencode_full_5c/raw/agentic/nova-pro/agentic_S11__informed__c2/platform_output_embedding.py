import os
from dashscope import Embeddings

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

embeddings = Embeddings(api_key=DASHSCOPE_API_KEY)


def embed_text(text):
    response = embeddings.create_embedding(text)
    return response.embedding
