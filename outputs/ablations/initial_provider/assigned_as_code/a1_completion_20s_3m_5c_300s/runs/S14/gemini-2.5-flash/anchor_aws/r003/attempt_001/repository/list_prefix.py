from storage_client import get_s3_client
from storage_models import ListPrefixPayload, ListPrefixResponse


def list_prefix(payload, config=None):
    config = config or {}
    client = get_s3_client(region_name=config.get("region"))
    prefix = payload["prefix"]
    max_keys = payload.get("max_keys", 100)

    response = client.list_objects_v2(Bucket=config["bucket"], Prefix=prefix, MaxKeys=max_keys)
    objects = []
    for obj in response.get("Contents", []):
        objects.append({"key": obj["Key"], "size": obj["Size"], "last_modified": obj["LastModified"].isoformat()})
    
    return ListPrefixResponse(prefix=prefix, objects=objects)
