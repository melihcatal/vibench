import boto3


def get_client(service_name, config=None):
    config = config or {}
    return boto3.client(service_name, region_name=config.get("region"))


def get_resource(service_name, config=None):
    config = config or {}
    return boto3.resource(service_name, region_name=config.get("region"))