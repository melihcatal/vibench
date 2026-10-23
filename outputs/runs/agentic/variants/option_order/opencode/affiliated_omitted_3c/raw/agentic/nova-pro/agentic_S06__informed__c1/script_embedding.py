import os
from dashscope import TextEmbedding


def embed_script(text):
    api_key = os.getenv("DASHSCOPE_API_KEY")
    response = TextEmbedding.call(
        model="text-embedding-v1", input=text, api_key=api_key
    )
    return response["output"]["embedding"]
