from google.cloud import aiplatform_v1

from translation_models import normalize_text


def translation_memory_embedding(text: str) -> dict:
    client = aiplatform_v1.PredictionServiceClient()
    return {"provider": "google", "text": normalize_text(text), "client": client.__class__.__name__}
