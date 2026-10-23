from __future__ import annotations

import os
from typing import Dict, List

from google.cloud import aiplatform_v1

from observability_models import EmbeddingResult


def _extract_vector(response: object) -> List[float]:
    values = getattr(response, "embeddings", None)
    if values:
        emb = values[0]
        return list(getattr(emb, "values", []))
    return []


def main(text: str | None = None) -> Dict[str, object]:
    text = text or os.getenv("LOG_TEXT", "")
    client = aiplatform_v1.PredictionServiceClient()
    endpoint = os.getenv("VERTEX_AI_EMBEDDING_ENDPOINT", "projects/PROJECT/locations/us-central1/endpoints/EMBEDDING_ENDPOINT")
    response = client.predict(endpoint=endpoint, instances=[{"content": text}])
    vector = _extract_vector(response)
    result = EmbeddingResult(
        provider="vertex-ai-text-embeddings-004",
        text=text,
        vector=vector,
        raw_response={"endpoint": endpoint},
    )
    return {"provider": result.provider, "dimensions": len(result.vector)}
