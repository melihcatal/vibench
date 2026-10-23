from google.cloud import storage


def list_objects_with_prefix(prefix, config=None):
    config = config or {}
    client = storage.Client(project=config["project_id"])
    blobs = client.list_blobs(config["bucket"], prefix=prefix)
    objects = [blob.name for blob in blobs]
    return {"objects": objects}