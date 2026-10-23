from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel


def asset_metadata_embedding(payload, config=None):
    config = config or {}
    aiplatform.init(project=config["project_id"], location=config.get("location", "us-central1"))
    model = TextEmbeddingModel.from_pretrained(config.get("model_id", "text-embedding-004"))
    text = payload.get("text", "")
    metadata = payload.get("metadata", {})
    source = f"{metadata}\n{text}".strip()
    embeddings = model.get_embeddings([source])
    return {"embedding": embeddings[0].values}
