from google.cloud import storage


def get_object_metadata(object_name, config=None):
    config = config or {}
    client = storage.Client(project=config["project_id"])
    blob = client.bucket(config["bucket"]).blob(object_name)
    metadata = blob.metadata
    return {"metadata": metadata}