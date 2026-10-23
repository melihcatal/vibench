from storage_client import get_blob_client


def presigned_download(payload, config=None):
    config = config or {}
    blob = get_blob_client(config, payload["object_name"])
    return {"url": blob.generate_signed_url(expiration=payload["expiration_seconds"], method="GET")}
