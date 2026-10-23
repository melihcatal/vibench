from datetime import timedelta

from storage_client import storage_bucket, load_config
from storage_models import normalize_object_name


def presigned_download(payload, config=None):
    config = load_config(config)
    bucket = storage_bucket(config)
    blob = bucket.blob(normalize_object_name(payload))
    return {"url": blob.generate_signed_url(expiration=timedelta(seconds=config["signed_url_expiration_seconds"]), version="v4", method="GET")}
