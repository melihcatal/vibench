import boto3


def get_database_client(config):
    return boto3.resource("dynamodb", region_name=config["region"])


def get_table(config):
    dynamodb = get_database_client(config)
    return dynamodb.Table(config["table_name"])