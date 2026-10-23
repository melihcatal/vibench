from google.cloud import aiplatform

from storage_client import storage_client


def asset_metadata_embedding(payload, config=None):
    _, config = storage_client(config)
    aiplatform.init(project=config["project_id"], location=config.get("location", "us-central1"))
    text = payload.get("text", "")
    metadata = payload.get("metadata", {})
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")
    embedding = model.get_embeddings([text + " " + str(metadata)])[0].values
    return {"embedding": embedding}
