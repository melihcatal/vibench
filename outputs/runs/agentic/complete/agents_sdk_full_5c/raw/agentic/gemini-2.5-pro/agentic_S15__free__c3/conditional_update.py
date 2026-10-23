from typing import Dict, Any
from botocore.exceptions import ClientError
from database_client import get_table

def conditional_update(
    document_id: str, 
    partition_key: str, 
    expected_version: int,
    update_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Applies a conditional update to a document in DynamoDB.

    The update succeeds only if the `documentVersion` attribute in the stored
    item matches the `expected_version`. The version is also incremented.

    Args:
        document_id: The ID of the document to update.
        partition_key: The partition key of the document.
        expected_version: The version number to check against.
        update_data: A dictionary of fields to update.

    Returns:
        The response from DynamoDB if successful.
        
    Raises:
        ValueError: if the conditional check fails.
    """
    table = get_table()
    
    update_expression_parts = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    # Build SET clause
    for key, value in update_data.items():
        # Use placeholders to avoid issues with reserved words
        attr_name_placeholder = f"#{key}"
        attr_value_placeholder = f":{key}"
        update_expression_parts.append(f"{attr_name_placeholder} = {attr_value_placeholder}")
        expression_attribute_values[attr_value_placeholder] = value
        expression_attribute_names[attr_name_placeholder] = key

    # Add version increment to the SET clause
    update_expression_parts.append("#docVer = :newVersion")
    expression_attribute_names["#docVer"] = "documentVersion"
    expression_attribute_values[":newVersion"] = expected_version + 1
    expression_attribute_values[":expectedVersion"] = expected_version
    
    update_expression = "SET " + ", ".join(update_expression_parts)
    
    try:
        response = table.update_item(
            Key={'partitionKey': partition_key, 'documentId': document_id},
            UpdateExpression=update_expression,
            ConditionExpression="#docVer = :expectedVersion",
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            raise ValueError("Conditional check failed: Document version mismatch.")
        else:
            raise
