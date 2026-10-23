import boto3

from storage_client import load_storage_config
from storage_models import normalize_object_name


def presigned_download(payload, config=None):
    cfg = load_storage_config(config)
    client = boto3.client("s3", region_name=cfg["region"])
    object_name = normalize_object_name(payload)
    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": cfg["bucket"], "Key": object_name},
        ExpiresIn=int(cfg["expires_in"]),
    )
    return {"object_name": object_name, "url": url, "expires_in": int(cfg["expires_in"]) }
