import boto3


def get_client(service):
    return boto3.client(service)


def get_resource(service):
    return boto3.resource(service)
