import boto3
from storage_client import get_s3_client
from storage_models import ListPrefixRequest

def list_objects_with_prefix(payload: ListPrefixRequest, config: dict = None) -> dict:
    config = config or {}
    s3_client = get_s3_client(config)
    
    bucket_name = payload.bucket or config["bucket"]
    
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=payload.prefix)
    
    objects = []
    if "Contents" in response:
        for obj in response["Contents"]:
            objects.append({"object_name": obj["Key"], "size": obj["Size"], "last_modified": obj["LastModified"].isoformat()})
            
    return {"objects": objects}
