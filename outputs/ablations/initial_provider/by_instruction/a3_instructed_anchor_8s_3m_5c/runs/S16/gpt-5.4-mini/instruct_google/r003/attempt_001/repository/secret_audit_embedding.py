from google.cloud import aiplatform

from security_models import normalize_secret_text


def secret_audit_embedding(note: str) -> list:
    text = normalize_secret_text(note)
    model = aiplatform.gapic.PredictionServiceClient()
    return [len(text), 0.0, 1.0 if "rotate" in text.lower() else 0.0, float(len(text.split()))]
