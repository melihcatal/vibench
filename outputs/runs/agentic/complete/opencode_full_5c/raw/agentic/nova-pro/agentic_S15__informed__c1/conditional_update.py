import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def conditional_update(table_name, key, update_expression, expression_attribute_values):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    try:
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW",
        )
        return response.get("Attributes")
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Error: {e}")
        return None
