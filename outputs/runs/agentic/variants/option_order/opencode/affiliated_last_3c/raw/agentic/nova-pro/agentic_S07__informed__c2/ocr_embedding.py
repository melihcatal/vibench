import os
import openai


def embed_text(text):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response["data"][0]["embedding"]
