from __future__ import annotations

from google.cloud import aiplatform_v1

from speech_models import normalize_text


MODEL_ID = "textembedding-gecko@003"


def embed_script(text: str, project: str, location: str = "us-central1") -> list[float]:
    """Embed narration scripts for voice-asset search using Vertex AI text embeddings."""
    client = aiplatform_v1.PredictionServiceClient()
    endpoint = f"projects/{project}/locations/{location}/publishers/google/models/{MODEL_ID}"
    instance = {"content": normalize_text(text)}
    response = client.predict(endpoint=endpoint, instances=[instance])
    prediction = response.predictions[0]
    values = prediction.get("embeddings", {}).get("values", []) if isinstance(prediction, dict) else []
    return list(values)
