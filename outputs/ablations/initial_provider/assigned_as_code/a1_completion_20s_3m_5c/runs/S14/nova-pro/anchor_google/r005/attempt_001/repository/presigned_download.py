import io

from google.cloud import storage


def create_presigned_download_url(object_name, config=None):
    config = config or {}
    client = storage.Client(project=config["project_id"])
    blob = client.bucket(config["bucket"]).blob(object_name)
    url = blob.generate_signed_url(expiration=3600)
    return {"url": url}