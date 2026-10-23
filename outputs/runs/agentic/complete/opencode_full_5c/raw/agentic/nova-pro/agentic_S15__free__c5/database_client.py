import boto3


def get_dynamodb_resource(region_name="us-west-2"):
    return boto3.resource("dynamodb", region_name=region_name)
