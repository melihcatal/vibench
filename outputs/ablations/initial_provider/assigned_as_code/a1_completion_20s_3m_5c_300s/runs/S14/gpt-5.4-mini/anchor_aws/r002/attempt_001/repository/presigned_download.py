from storage_client import get_s3_client, get_storage_config
from storage_models import normalize_key


def presigned_download(payload, config=None):
    config = get_storage_config(config)
    client = get_s3_client(config)
    return {"url": client.generate_presigned_url("get_object", Params={"Bucket": config["bucket"], "Key": normalize_key(payload)}, ExpiresIn=payload.get("expires_in", 3600))}
