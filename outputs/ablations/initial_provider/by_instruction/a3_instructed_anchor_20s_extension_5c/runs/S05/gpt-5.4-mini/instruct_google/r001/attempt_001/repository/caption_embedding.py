from google.cloud import aiplatform


def caption_embedding(text: str) -> list[float]:
    client = aiplatform.gapic.PredictionServiceClient()
    endpoint = "projects/0/locations/us-central1/publishers/google/models/text-embedding-004"
    response = client.predict(endpoint=endpoint, instances=[{"content": text}])
    pred = response.predictions[0] if response.predictions else {}
    return list(pred.get("embeddings", pred.get("values", [])))
