import boto3


def get_dynamodb_client(region, table_name):
    return boto3.resource("dynamodb", region_name=region).Table(table_name)