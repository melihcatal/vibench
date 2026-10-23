import boto3
import os

def conditional_update_document(
    table_name: str,
    key: dict,
    update_expression: str,
    condition_expression: str,
    expression_attribute_values: dict = None,
    expression_attribute_names: dict = None
) -> dict:
    """
    Applies a conditional or version-aware update to one stored document in AWS DynamoDB.

    Args:
        table_name (str): The name of the DynamoDB table.
        key (dict): A dictionary representing the primary key of the item to update.
                    e.g., {'id': 'document-123'}
        update_expression (str): The update expression to apply.
                                  e.g., "SET #status = :new_status"
        condition_expression (str): The condition expression that must be satisfied for the update to proceed.
                                    e.g., "attribute_exists(id) AND #version = :expected_version"
        expression_attribute_values (dict, optional): A dictionary of substitution tokens for attribute values.
                                                      e.g., {':new_status': 'processed', ':expected_version': 1}
        expression_attribute_names (dict, optional): A dictionary of substitution tokens for attribute names.
                                                     e.g., {'#status': 'document_status', '#version': 'version'}

    Returns:
        dict: The response from the DynamoDB update_item operation.
    """
    dynamodb = boto3.client('dynamodb', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

    try:
        response = dynamodb.update_item(
            TableName=table_name,
            Key=key,
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="UPDATED_NEW"
        )
        return response
    except dynamodb.exceptions.ConditionalCheckFailedException:
        print("Conditional check failed: The document either does not exist or the condition was not met.")
        return {"error": "ConditionalCheckFailedException"}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

