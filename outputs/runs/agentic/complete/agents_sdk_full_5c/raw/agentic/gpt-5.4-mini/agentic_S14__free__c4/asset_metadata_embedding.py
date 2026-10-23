from __future__ import annotations

from typing import List

from openai import OpenAI

from storage_client import get_bucket_name, get_s3_client
from storage_models import EmbeddingResult, ObjectRef, safe_join_text

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def asset_metadata_embedding(key: str) -> EmbeddingResult:
    s3 = get_s3_client()
    bucket = get_bucket_name()
    head = s3.head_object(Bucket=bucket, Key=key)
    obj = s3.get_object(Bucket=bucket, Key=key)
    text = obj["Body"].read().decode("utf-8", errors="replace")
    metadata_text = safe_join_text([f"{k}: {v}" for k, v in (head.get("Metadata") or {}).items()])
    input_text = safe_join_text([metadata_text, text[:6000]])

    client = OpenAI()
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=input_text)
    vector: List[float] = list(response.data[0].embedding)
    return EmbeddingResult(source=ObjectRef(bucket=bucket, key=key), vector=vector, dimension=len(vector), provider=OPENAI_EMBEDDING_MODEL)
