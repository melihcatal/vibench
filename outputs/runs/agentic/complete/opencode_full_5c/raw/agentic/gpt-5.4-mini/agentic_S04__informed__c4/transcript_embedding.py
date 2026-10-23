from openai import OpenAI

from speech_client import openai_client_kwargs


def transcript_embedding(text: str):
    client = OpenAI(**openai_client_kwargs())
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
