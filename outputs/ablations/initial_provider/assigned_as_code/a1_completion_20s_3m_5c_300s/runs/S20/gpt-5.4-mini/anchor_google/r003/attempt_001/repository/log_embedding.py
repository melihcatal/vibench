from google.cloud import aiplatform


def log_embedding(payload, config=None):
    client = aiplatform.gapic.PredictionServiceClient()
    text = payload["text"]
    endpoint = payload["endpoint"]
    instance = {"content": text}
    response = client.predict(endpoint=endpoint, instances=[instance])
    return {"embedding": list(response.predictions[0].get("embeddings", response.predictions[0]))}
