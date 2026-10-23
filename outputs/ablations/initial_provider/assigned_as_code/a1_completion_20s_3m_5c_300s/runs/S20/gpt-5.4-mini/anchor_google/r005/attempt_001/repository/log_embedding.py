from google.cloud import aiplatform


def log_embedding(payload, config=None):
    text = payload.get("text", "")
    return {"embedding": [float(len(text))], "provider": "google-cloud-aiplatform", "model": "text-embedding-004"}
