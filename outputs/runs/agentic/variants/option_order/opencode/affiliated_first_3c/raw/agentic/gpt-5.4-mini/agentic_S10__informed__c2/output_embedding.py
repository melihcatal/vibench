import os
from openai import OpenAI
from model_models import normalize_text


def output_embedding(text: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.embeddings.create(
        model="text-embedding-3-large", input=normalize_text(text)
    )
    return resp.data[0].embedding
