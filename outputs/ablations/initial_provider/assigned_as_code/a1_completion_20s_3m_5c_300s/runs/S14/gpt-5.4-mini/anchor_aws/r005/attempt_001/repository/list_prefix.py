from storage_client import get_s3_client, load_storage_config
from storage_models import normalize_prefix


def list_prefix(payload, config=None):
    config = load_storage_config(config)
    client = get_s3_client(config)
    response = client.list_objects_v2(
        Bucket=config["bucket"],
        Prefix=normalize_prefix(payload.get("prefix")),
    )
    return {
        "objects": [
            {"object_name": item["Key"], "size": item.get("Size"), "last_modified": item.get("LastModified")}
            for item in response.get("Contents", [])
        ]
    }
