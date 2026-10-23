import boto3


def get_observability_client(region):
    return boto3.client("cloudwatch", region_name=region)


def get_config(namespace, dimensions=None):
    return {"namespace": namespace, "dimensions": dimensions or {}}