import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-west-2")


def get_table(table_name):
    return dynamodb.Table(table_name)
