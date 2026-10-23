import boto3


def get_object_metadata(object_name, config=None):
    config = config or {}
    client = boto3.client("s3", region_name=config.get("region"))
    metadata = client.head_object(Bucket=config['bucket'], Key=object_name)
    return metadata