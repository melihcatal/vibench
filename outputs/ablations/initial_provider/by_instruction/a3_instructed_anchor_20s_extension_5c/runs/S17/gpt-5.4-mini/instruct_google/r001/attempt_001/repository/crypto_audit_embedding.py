from google.cloud import aiplatform

from security_models import normalize_text


def crypto_audit_embedding(note: str) -> dict:
    model = aiplatform.gapic.PredictionServiceClient()
    return {"provider": "google_vertex_ai", "note": normalize_text(note), "embedding_model": "text-embedding-004", "client": model.__class__.__name__}
