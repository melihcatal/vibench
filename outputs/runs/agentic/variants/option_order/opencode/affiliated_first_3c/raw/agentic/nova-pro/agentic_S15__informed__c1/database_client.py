import boto3


def get_dynamodb_client():
    return boto3.client("dynamodb")


def get_table(table_name):
    dynamodb = boto3.resource("dynamodb")
    return dynamodb.Table(table_name)
