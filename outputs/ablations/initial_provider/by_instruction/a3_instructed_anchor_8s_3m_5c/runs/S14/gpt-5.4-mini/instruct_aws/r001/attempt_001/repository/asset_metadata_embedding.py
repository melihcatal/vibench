from openai import OpenAI

from storage_client import default_embedding_model
from storage_models import EmbeddingResponse


def asset_metadata_embedding(metadata_text: str, extracted_text: str, bucket: str, key: str) -> EmbeddingResponse:
    client = OpenAI()
    model = default_embedding_model()
    payload = f"Metadata:\n{metadata_text}\n\nText:\n{extracted_text}"
    result = client.embeddings.create(model=model, input=payload)
    vector = result.data[0].embedding if result.data else []
    return EmbeddingResponse(bucket=bucket, key=key, vector=vector)
