import io

from google.cloud import storage


def upload_object(payload, config=None):
    config = config or {}
    client = storage.Client(project=config["project_id"])
    blob = client.bucket(config["bucket"]).blob(payload["object_name"])
    blob.upload_from_file(io.BytesIO(payload["data"]), content_type=payload.get("content_type", "application/octet-stream"))
    return {"object_name": payload["object_name"]}
