import os
from dashscope import TextEmbedding


def embed_metadata(text):
    response = TextEmbedding.call(
        model="text-embedding-v1",
        input=text,
        api_key=os.getenv("DASHSCOPE_API_KEY"),
    )
    return response["output"]["embedding"]
