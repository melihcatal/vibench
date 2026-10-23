import boto3
from botocore.exceptions import ClientError

def conditional_update_document(table_name: str, document_id: str, update_attributes: dict, condition_expression: str) -> dict:
    """
    Applies a conditional or version-aware update to one stored document in AWS DynamoDB.

    Args:
        table_name (str): The name of the DynamoDB table.
        document_id (str): The primary identifier (partition key) of the document to update.
        update_attributes (dict): A dictionary of attributes to update.
                                 Example: {'attribute_name': {'Value': 'new_value', 'Action': 'PUT'}}
        condition_expression (str): The condition that must be satisfied for the update to proceed.
                                    Example for version-aware: 'attribute_exists(version) AND version = :current_version'

    Returns:
        dict: The response from the DynamoDB update_item operation or an error message.
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Prepare UpdateExpression and ExpressionAttributeValues
    update_expression_parts = []
    expression_attribute_values = {}
    expression_attribute_names = {}
    for i, (key, value) in enumerate(update_attributes.items()):
        update_expression_parts.append(f'#{key} = :new_{key}')
        expression_attribute_values[f':new_{key}'] = value
        expression_attribute_names[f'#{key}'] = key
    
    update_expression = 'SET ' + ', '.join(update_expression_parts)

    try:
        response = table.update_item(
            Key={
                'id': document_id  # Assuming 'id' is the primary key
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ConditionExpression=condition_expression,
            ReturnValues='UPDATED_NEW'
        )
        return response
    except ClientError as e:
        return {'error': e.response['Error']['Message']}

