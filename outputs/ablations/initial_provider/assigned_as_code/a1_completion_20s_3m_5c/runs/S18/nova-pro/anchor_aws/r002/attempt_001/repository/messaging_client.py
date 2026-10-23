import boto3


def get_client(service_name, region_name=None):
    return boto3.client(service_name, region_name=region_name)


def get_resource(service_name, region_name=None):
    return boto3.resource(service_name, region_name=region_name)