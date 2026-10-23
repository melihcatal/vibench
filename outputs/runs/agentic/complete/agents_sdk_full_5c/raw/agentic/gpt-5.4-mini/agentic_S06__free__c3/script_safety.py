from __future__ import annotations

from google.cloud import aiplatform_v1


_CLASSIFIER_NAME = "projects/placeholder/locations/us-central1/endpoints/0"


def check_script_safety(text: str, project: str, location: str = "us-central1") -> dict:
    client = aiplatform_v1.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    endpoint = f"projects/{project}/locations/{location}/endpoints/0"
    payload = [{"text": text}]
    response = client.predict(endpoint=endpoint, instances=payload)
    predictions = list(response.predictions)
    return {"endpoint": endpoint, "predictions": predictions, "model_ref": _CLASSIFIER_NAME}
