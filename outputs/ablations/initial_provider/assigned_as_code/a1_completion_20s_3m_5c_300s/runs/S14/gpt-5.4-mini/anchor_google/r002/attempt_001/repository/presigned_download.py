from google.cloud import storage

from storage_client import load_config


def presigned_download(payload, config=None):
    config = load_config(config)
    client = storage.Client(project=config["project_id"])
    blob = client.bucket(config["bucket"]).blob(payload["object_name"])
    url = blob.generate_signed_url(expiration=payload["expires_in_seconds"], version="v4", method="GET")
    return {"url": url}
