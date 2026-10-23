from storage_client import get_s3_client, get_storage_config
from storage_models import normalize_key


def object_metadata(payload, config=None):
    config = get_storage_config(config)
    client = get_s3_client(config)
    response = client.head_object(Bucket=config["bucket"], Key=normalize_key(payload))
    return {"metadata": response, "object_name": normalize_key(payload)}
