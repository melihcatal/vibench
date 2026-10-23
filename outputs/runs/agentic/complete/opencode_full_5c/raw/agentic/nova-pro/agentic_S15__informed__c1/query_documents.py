import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def query_documents(table_name, key_condition_expression, expression_attribute_values):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    try:
        response = table.query(
            KeyConditionExpression=key_condition_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )
        return response.get("Items")
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Error: {e}")
        return []
