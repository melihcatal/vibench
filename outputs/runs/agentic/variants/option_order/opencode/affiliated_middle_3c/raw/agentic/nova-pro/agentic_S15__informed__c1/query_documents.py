import os
import boto3

DYNAMODB_TABLE = "example-table"


def query_documents(field_name, field_value):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(DYNAMODB_TABLE)
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Attr(field_name).eq(field_value)
    )
    return response["Items"]


if __name__ == "__main__":
    documents = query_documents("name", "example")
    print(documents)
