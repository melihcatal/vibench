from google.cloud import storage

from storage_client import get_storage_client
from storage_models import ObjectMetadataRequest


def stored_asset_summary(request: ObjectMetadataRequest) -> dict:
    client = get_storage_client()
    text = client.bucket(request.bucket).blob(request.name).download_as_text()
    summary = text[:280]
    return {"bucket": request.bucket, "name": request.name, "summary": summary}
