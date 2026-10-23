from google.cloud import aiplatform

from security_client import load_config


def crypto_audit_embedding(payload, config=None):
    config = load_config(config)
    aiplatform.init(project=config["project_id"], location=config["location"])
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    text = payload.get("note", "")
    embeddings = model.get_embeddings([text])
    return {"embedding": embeddings[0].values}
