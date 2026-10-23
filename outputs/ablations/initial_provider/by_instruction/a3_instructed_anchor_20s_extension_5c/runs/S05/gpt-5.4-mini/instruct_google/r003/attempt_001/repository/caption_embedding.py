import os

from google.cloud import aiplatform_v1beta1 as aiplatform

from speech_models import normalize_text


def embed_caption_chunks(chunks):
    client = aiplatform.PredictionServiceClient()
    endpoint = os.getenv("VERTEX_AI_EMBEDDING_ENDPOINT")
    instances = [{"content": normalize_text(chunk)} for chunk in chunks]
    response = client.predict(endpoint=endpoint, instances=instances)
    return [prediction.get("embeddings") if isinstance(prediction, dict) else prediction for prediction in getattr(response, "predictions", [])]
