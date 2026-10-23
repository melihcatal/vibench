import os

from google.cloud import aiplatform_v1beta1 as aiplatform

from speech_models import normalize_text


def summarize_meeting(chunks):
    client = aiplatform.PredictionServiceClient()
    endpoint = os.getenv("VERTEX_AI_SUMMARY_ENDPOINT")
    instances = [{"content": normalize_text(chunk)} for chunk in chunks]
    response = client.predict(endpoint=endpoint, instances=instances)
    predictions = getattr(response, "predictions", [])
    if predictions:
        first = predictions[0]
        if isinstance(first, dict) and "summary" in first:
            return first["summary"]
        return str(first)
    return ""
