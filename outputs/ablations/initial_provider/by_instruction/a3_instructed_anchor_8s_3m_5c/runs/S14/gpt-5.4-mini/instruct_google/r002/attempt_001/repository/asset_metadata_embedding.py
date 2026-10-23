from google.cloud import storage
from google.cloud import aiplatform

from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest


def asset_metadata_embedding(request: ObjectMetadataRequest) -> dict:
    client = get_storage_client()
    blob = client.bucket(request.bucket).blob(request.name)
    blob.reload()
    text = blob.download_as_text() if blob.size else ""
    content = f"bucket={request.bucket}\nname={request.name}\nsize={blob.size}\ncontent_type={blob.content_type}\nmetadata={dict(blob.metadata or {})}\ntext={text}"
    return {"bucket": request.bucket, "name": request.name, "embedding_source": "google.cloud.aiplatform", "content": content}
