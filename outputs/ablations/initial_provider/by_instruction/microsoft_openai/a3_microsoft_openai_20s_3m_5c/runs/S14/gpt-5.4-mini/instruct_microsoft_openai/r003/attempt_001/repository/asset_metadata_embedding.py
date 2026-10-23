import os

from openai import OpenAI

from storage_models import EmbeddingResult


def asset_metadata_embedding(text: str):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model="text-embedding-3-large", input=text)
    return EmbeddingResult(text=text, embedding=response.data[0].embedding, raw={"model": "text-embedding-3-large"})
