from __future__ import annotations

from google.cloud import aiplatform_v1


def embed_script(text: str, project: str, location: str = "us-central1", model: str = "textembedding-gecko@003") -> list[float]:
    client = aiplatform_v1.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    endpoint = f"projects/{project}/locations/{location}/publishers/google/models/{model}"
    response = client.predict(endpoint=endpoint, instances=[{"content": text}])
    if not response.predictions:
        return []
    vector = response.predictions[0].get("embeddings", {}).get("values", [])
    return list(vector)
