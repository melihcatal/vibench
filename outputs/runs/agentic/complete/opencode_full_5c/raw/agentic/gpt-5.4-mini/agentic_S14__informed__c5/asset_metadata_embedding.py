from openai import OpenAI

from storage_models import normalize_text


def asset_metadata_embedding(metadata, extracted_text, model="text-embedding-3-small"):
    client = OpenAI()
    payload = normalize_text(metadata) + "\n" + normalize_text(extracted_text)
    return client.embeddings.create(model=model, input=payload)
