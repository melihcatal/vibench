import base64

from google.cloud import storage


def image_asset_archive(payload, config=None):
    config = config or {}
    client = storage.Client()
    bucket = client.bucket(config["bucket"])
    name = config.get("object_name", "image-analysis-artifacts.json")
    blob = bucket.blob(name)
    data = payload.get("artifact")
    if isinstance(data, bytes):
        content = data
    else:
        content = base64.b64encode(str(data).encode("utf-8"))
    blob.upload_from_string(content)
    return {"bucket": config["bucket"], "object_name": name}
