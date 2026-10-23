import os
import boto3

DYNAMODB_TABLE = "example-table"


def conditional_update(document_id, update_expression, expression_attribute_values):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(DYNAMODB_TABLE)
    table.update_item(
        Key={"id": document_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ConditionExpression="attribute_exists(id)",
    )


if __name__ == "__main__":
    conditional_update("example-id", "SET value = :val", {":val": 456})
