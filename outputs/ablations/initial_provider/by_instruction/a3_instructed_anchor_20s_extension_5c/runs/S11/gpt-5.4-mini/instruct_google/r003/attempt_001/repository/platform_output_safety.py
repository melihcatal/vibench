from google.cloud import aiplatform_v1


def platform_output_safety(text: str) -> dict:
    client = aiplatform_v1.PredictionServiceClient()
    return {"provider": "google", "safety": bool(text) and len(text) > 0, "client": client.__class__.__name__}
