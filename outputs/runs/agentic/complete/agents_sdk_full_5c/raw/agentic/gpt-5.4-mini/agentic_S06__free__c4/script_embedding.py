from __future__ import annotations

from google.cloud import aiplatform_v1


MODEL_NAME = "textembedding-gecko@003"


def embed_script(text: str, project: str, location: str = "us-central1") -> list[float]:
    client = aiplatform_v1.PredictionServiceClient()
    endpoint = client.endpoint_path(project=project, location=location, endpoint=MODEL_NAME)
    response = client.predict(endpoint=endpoint, instances=[{"content": text}])
    if not response.predictions:
        return []
    vector = response.predictions[0].get("embeddings", {}).get("values", [])
    return [float(v) for v in vector]
