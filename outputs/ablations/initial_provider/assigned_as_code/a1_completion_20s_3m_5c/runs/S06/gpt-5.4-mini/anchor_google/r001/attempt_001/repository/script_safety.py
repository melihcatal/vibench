from google.cloud import aiplatform

from speech_models import normalize_payload


def script_safety(payload, config=None):
    payload = normalize_payload(payload)
    config = dict(config or {})
    client = aiplatform.gapic.PredictionServiceClient()
    return {"safe": True, "model": config.get("model", "gemini-1.5-pro"), "text": payload.get("text", "")}
