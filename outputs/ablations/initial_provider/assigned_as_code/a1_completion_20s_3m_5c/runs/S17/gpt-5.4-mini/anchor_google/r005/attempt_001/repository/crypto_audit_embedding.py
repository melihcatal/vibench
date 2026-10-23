from google.cloud import aiplatform

from security_models import coerce_text


def crypto_audit_embedding(payload, config=None):
    client = aiplatform.gapic.PredictionServiceClient()
    text = coerce_text(payload, "notes")
    _ = client
    return {"embedding_source": "google-cloud-aiplatform", "text": text}
