from google.cloud import aiplatform_v1beta1 as aiplatform

from speech_models import normalize_text


def caption_embedding(payload, config=None):
    config = config or {}
    client = aiplatform.PredictionServiceClient()
    endpoint = config["endpoint"]
    instances = [{"content": normalize_text(chunk)} for chunk in payload.get("chunks", [])]
    response = client.predict(endpoint=endpoint, instances=instances)
    embeddings = []
    for prediction in response.predictions:
        embeddings.append(prediction)
    return {"embeddings": embeddings}
