import boto3


def list_objects_with_prefix(prefix, config=None):
    config = config or {}
    client = boto3.client("s3", region_name=config.get("region"))
    objects = client.list_objects_v2(Bucket=config['bucket'], Prefix=prefix)
    return objects['Contents']