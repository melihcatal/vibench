import os

from google.cloud import aiplatform


def embed_caption(text: str):
    aiplatform.init()
    model_name = os.getenv("GOOGLE_EMBEDDING_MODEL", "text-embedding-004")
    model = aiplatform.TextEmbeddingModel.from_pretrained(model_name)
    return model.get_embeddings([text])[0].values
