from google.cloud import aiplatform

from storage_client import storage_bucket, load_config, aiplatform_client
from storage_models import normalize_object_name


def asset_metadata_embedding(payload, config=None):
    config = load_config(config)
    blob = storage_bucket(config).blob(normalize_object_name(payload))
    blob.reload()
    text = (payload or {}).get("text", "")
    content = " ".join(filter(None, [blob.name, blob.content_type or "", str(blob.size or ""), text]))
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings([content])
    return {"embedding": embeddings[0].values if embeddings else []}
