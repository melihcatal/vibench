from google.cloud import aiplatform

from speech_client import embedding_model


def caption_embedding(payload, config=None):
    config = config or {}
    model = embedding_model()
    text = payload["text"]
    embedding = model.get_embeddings([text])[0].values
    return {"embedding": embedding, "model": "text-embedding-004"}
