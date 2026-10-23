from storage_client import get_storage_client


def presigned_download(object_name, config=None):
    client = get_storage_client(config)
    blob = client.bucket(config["bucket"]).blob(object_name)
    url = blob.generate_signed_url(expiration=3600)
    return {"url": url}