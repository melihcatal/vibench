from google.cloud import storage
from google.cloud import aiplatform

from storage_client import get_bucket
from storage_models import DocumentInsight, normalize_object_name


def asset_metadata_embedding(bucket_name: str, object_name: str) -> dict:
    bucket = get_bucket(bucket_name)
    blob = bucket.blob(normalize_object_name(object_name))
    blob.reload()
    text = blob.download_as_text() if blob.size and blob.size < 1000000 else ""
    instance = {"content": f"{blob.name}\n{blob.content_type or ''}\n{text}"}
    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")
    embeddings = model.get_embeddings([instance["content"]])
    vector = embeddings[0].values if embeddings else None
    return DocumentInsight(bucket=bucket_name, name=blob.name, text=text, embedding=vector).to_dict()
