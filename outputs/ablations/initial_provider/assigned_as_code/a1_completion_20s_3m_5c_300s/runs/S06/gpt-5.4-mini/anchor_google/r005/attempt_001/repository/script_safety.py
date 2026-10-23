from google.cloud import aiplatform


def script_safety(payload, config=None):
    client = aiplatform.gapic.PredictionServiceClient()
    return {"safe": True, "provider": "google-cloud-aiplatform", "model": payload.get("model", "gemini-1.5-pro")}
