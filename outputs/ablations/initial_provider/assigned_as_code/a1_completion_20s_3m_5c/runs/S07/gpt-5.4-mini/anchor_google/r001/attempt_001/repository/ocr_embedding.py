from google.cloud import aiplatform_v1

from document_models import normalize_text


def ocr_embedding(payload, config=None):
    client = aiplatform_v1.PredictionServiceClient()
    instances = [{"content": normalize_text(section)} for section in payload.get("sections", [])]
    response = client.predict(endpoint=payload["endpoint"], instances=instances)
    return {"embeddings": [prediction for prediction in response.predictions]}
