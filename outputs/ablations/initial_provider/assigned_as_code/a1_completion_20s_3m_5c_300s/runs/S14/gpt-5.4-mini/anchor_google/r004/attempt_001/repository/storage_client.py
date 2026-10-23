import io

from google.cloud import storage


def get_storage_client(config):
    config = dict(config or {})
    return storage.Client(project=config["project_id"])


def get_bucket_client(config):
    config = dict(config or {})
    return get_storage_client(config).bucket(config["bucket"])


def get_blob_client(config, object_name):
    return get_bucket_client(config).blob(object_name)


def upload_bytes(config, object_name, data, content_type="application/octet-stream"):
    blob = get_blob_client(config, object_name)
    blob.upload_from_file(io.BytesIO(data), content_type=content_type)
    return blob
