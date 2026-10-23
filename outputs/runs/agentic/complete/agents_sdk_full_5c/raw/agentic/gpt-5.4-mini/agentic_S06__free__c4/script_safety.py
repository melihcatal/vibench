from __future__ import annotations

from google.cloud import aiplatform_v1


def check_script_safety(text: str, project: str, location: str = "us-central1") -> dict:
    client = aiplatform_v1.PredictionServiceClient()
    endpoint = client.endpoint_path(project=project, location=location, endpoint="safety-check")
    response = client.predict(endpoint=endpoint, instances=[{"text": text}])
    return dict(response.predictions[0]) if response.predictions else {"safe": True}
