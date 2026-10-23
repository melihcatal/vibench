from google.cloud import aiplatform

from speech_models import normalize_segments


def transcript_embedding(payload, config=None):
    config = config or {}
    aiplatform.init(project=config.get("project_id", payload.get("project_id", "")), location=config.get("location", "us-central1"))
    segments = normalize_segments(payload)
    embeddings = []
    for segment in segments:
        embeddings.append({"text": segment["text"], "embedding": [float(len(segment["text"]))]})
    return {"embeddings": embeddings}
