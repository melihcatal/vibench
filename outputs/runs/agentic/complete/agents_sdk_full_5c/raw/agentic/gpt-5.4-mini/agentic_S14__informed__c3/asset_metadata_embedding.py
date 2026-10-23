from __future__ import annotations

from openai import OpenAI

from storage_models import EmbeddingRequest, EmbeddingResult, normalize_mapping


EMBEDDING_MODEL_ID = "text-embedding-3-small"


def embed_object_metadata_and_text(request: EmbeddingRequest) -> EmbeddingResult:
    client = OpenAI()
    metadata = normalize_mapping(request.metadata)
    combined = [f"bucket: {request.bucket}", f"key: {request.key}"]
    combined.extend(f"{k}: {v}" for k, v in metadata.items())
    if request.extracted_text:
        combined.append(request.extracted_text)
    response = client.embeddings.create(model=EMBEDDING_MODEL_ID, input="\n".join(combined))
    vector = list(response.data[0].embedding)
    return EmbeddingResult(vector=vector, dimensions=len(vector), raw=response.model_dump())
