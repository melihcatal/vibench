import boto3


def get_dynamodb_client(config):
    return boto3.client("dynamodb", region_name=config.get("region"))