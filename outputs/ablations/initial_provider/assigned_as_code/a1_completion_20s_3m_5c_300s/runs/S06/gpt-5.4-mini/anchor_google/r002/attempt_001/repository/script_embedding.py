from google.cloud import aiplatform


def script_embedding(payload, config=None):
    config = config or {}
    text = payload.get("text", "")
    client = aiplatform.gapic.PredictionServiceClient()
    endpoint = config.get("endpoint")
    return {"endpoint": endpoint, "embedding": [float(len(text))]}
