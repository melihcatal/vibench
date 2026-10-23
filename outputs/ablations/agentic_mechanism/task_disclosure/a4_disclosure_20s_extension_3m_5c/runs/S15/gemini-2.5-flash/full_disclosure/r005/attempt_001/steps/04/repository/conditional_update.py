
import boto3
from botocore.exceptions import ClientError

def conditional_update_document(
    table_name: str,
    key: dict,
    update_expression: str,
    expression_attribute_values: dict,
    condition_expression: str,
) -> dict:
    """
    Applies a conditional or version-aware update to one stored document in AWS DynamoDB.

    Args:
        table_name (str): The name of the DynamoDB table.
        key (dict): A dictionary representing the primary key of the item to update.
        update_expression (str): The update expression to apply to the item.
        expression_attribute_values (dict): A dictionary of values for the expression attributes.
        condition_expression (str): The condition expression that must be satisfied for the update to proceed.

    Returns:
        dict: The response from the DynamoDB update_item operation.
    """
    dynamodb = boto3.client("dynamodb")  # AWS DynamoDB client

    try:
        response = dynamodb.update_item(
            TableName=table_name,
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ConditionExpression=condition_expression,
            ReturnValues="UPDATED_NEW",
        )
        return response
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print("Conditional check failed: The document could not be updated.")
            raise
        else:
            raise
