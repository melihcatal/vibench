import boto3
import os

def conditional_update_document(
    table_name: str,
    document_id: str,
    update_expression: str,
    expression_attribute_values: dict,
    condition_expression: str,
    region_name: str = None
):
    """
    Applies a conditional or version-aware update to one stored document in AWS DynamoDB.

    Args:
        table_name (str): The name of the DynamoDB table.
        document_id (str): The primary identifier of the document to update.
        update_expression (str): The update expression to apply.
        expression_attribute_values (dict): Dictionary of values for the update expression.
        condition_expression (str): The condition expression that must be satisfied for the update to proceed.
        region_name (str, optional): The AWS region. Defaults to None, will use environment variable or default config.

    Returns:
        dict: The response from the DynamoDB update_item operation.
    """
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1") # Default to us-east-1 if not specified

    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table = dynamodb.Table(table_name)

    response = table.update_item(
        Key={
            'id': document_id  # Assuming 'id' is the primary key
        },
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ConditionExpression=condition_expression,
        ReturnValues="UPDATED_NEW"
    )
    return response

