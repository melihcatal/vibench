from google.cloud import aiplatform


def script_embedding(payload, config=None):
    client = aiplatform.gapic.PredictionServiceClient()
    return {"embedding": [0.0], "model": payload.get("model", "text-embedding-004")}
