from __future__ import annotations

from google.cloud import aiplatform_v1


def embed_script(text: str, project: str, location: str = "us-central1", model: str = "textembedding-gecko@003") -> list[float]:
    client = aiplatform_v1.PredictionServiceClient()
    endpoint = client.endpoint_path(project=project, location=location, endpoint=model)
    response = client.predict(
        endpoint=endpoint,
        instances=[{"content": text}],
        parameters={"auto_truncate": True},
    )
    prediction = response.predictions[0]
    if isinstance(prediction, dict) and "embeddings" in prediction:
        return list(prediction["embeddings"]["values"])
    if isinstance(prediction, dict) and "values" in prediction:
        return list(prediction["values"])
    return list(prediction)
