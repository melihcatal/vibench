import os
import boto3

dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def store_message(table_name, message):
    table = dynamodb.Table(table_name)
    table.put_item(Item=message)
