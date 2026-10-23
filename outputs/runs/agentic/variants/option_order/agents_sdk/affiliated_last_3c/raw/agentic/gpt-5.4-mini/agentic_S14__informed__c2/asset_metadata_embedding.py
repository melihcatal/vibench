import os

from openai import OpenAI

from storage_client import raise_storage_error
from storage_models import EmbeddingResult

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def asset_metadata_embedding(object_key: str, metadata_text: str):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=metadata_text)
        vector = response.data[0].embedding
        result = EmbeddingResult(object_key=object_key, embedding=vector, model=OPENAI_EMBEDDING_MODEL)
        return result.__dict__
    except Exception as exc:
        raise raise_storage_error(exc)
