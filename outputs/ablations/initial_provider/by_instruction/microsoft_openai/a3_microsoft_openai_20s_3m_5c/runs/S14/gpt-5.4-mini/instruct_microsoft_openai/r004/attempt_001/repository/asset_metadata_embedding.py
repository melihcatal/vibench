import os

from openai import OpenAI


def asset_metadata_embedding(metadata: str, extracted_text: str):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    payload = f"Metadata: {metadata}\nText: {extracted_text}"
    return client.embeddings.create(model="text-embedding-3-large", input=payload)
