from storage_client import get_blob_client


def object_metadata(payload, config=None):
    config = config or {}
    blob = get_blob_client(config, payload["object_name"])
    blob.reload()
    return {"object_name": payload["object_name"], "size": blob.size, "content_type": blob.content_type, "etag": blob.etag}
