from storage_client import get_bucket_name, get_s3_client, load_storage_config
from storage_models import normalize_object_name


def presigned_download(payload, config=None):
    config = load_storage_config(config)
    client = get_s3_client(config)
    return {"url": client.generate_presigned_url("get_object", Params={"Bucket": get_bucket_name(config), "Key": normalize_object_name(payload["object_name"])}, ExpiresIn=config["expires_in"])}
