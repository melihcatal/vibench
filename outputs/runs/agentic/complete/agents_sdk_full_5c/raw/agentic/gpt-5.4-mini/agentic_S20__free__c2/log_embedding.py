from __future__ import annotations

from google.cloud import aiplatform_v1


def embed_log_message(text: str) -> list[float]:
    client = aiplatform_v1.PredictionServiceClient()
    endpoint = "projects/sample-project/locations/us-central1/endpoints/1234567890123456789"
    response = client.predict(endpoint=endpoint, instances=[{"content": text}])
    if response.predictions:
        pred = response.predictions[0]
        if isinstance(pred, dict) and "embeddings" in pred:
            return list(pred["embeddings"])
    return []
