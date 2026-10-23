import datetime
from database_client import get_dynamodb_resource
from database_models import Document
from typing import Dict, Any

def conditional_update(table_name: str, document_id: str, updates: Dict[str, Any], expected_version: int) -> Dict[str, Any]:
    """
    Applies a conditional or version-aware update to one stored document in DynamoDB.
    This uses optimistic locking based on a document version.
    """
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)

    current_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Prepare UpdateExpression and ExpressionAttributeValues
    update_expression_parts = []
    expression_attribute_values = {':expected_version': expected_version}
    expression_attribute_names = {}

    # Increment version automatically
    new_version = expected_version + 1
    update_expression_parts.append("SET #v = :new_version")
    expression_attribute_names["#v"] = "version"
    expression_attribute_values[":new_version"] = new_version

    # Update updated_at timestamp
    update_expression_parts.append("#ua = :updated_at")
    expression_attribute_names["#ua"] = "updated_at"
    expression_attribute_values[":updated_at"] = current_time


    for k, v in updates.items():
        # Avoid updating the id or version directly through 'updates' param
        if k != "id" and k != "version" and k != "created_at" and k != "updated_at":
            placeholder_key = f"#attr_{k}"
            placeholder_value = f":val_{k}"
            update_expression_parts.append(f"{placeholder_key} = {placeholder_value}")
            expression_attribute_names[placeholder_key] = k
            expression_attribute_values[placeholder_value] = v

    update_expression = "SET " + ", ".join(update_expression_parts)

    try:
        response = table.update_item(
            Key={'id': document_id},
            UpdateExpression=update_expression,
            ConditionExpression="attribute_exists(id) AND #v = :expected_version",
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return response.get('Attributes', {})
    except Exception as e:
        if "ConditionalCheckFailedException" in str(e):
            raise ValueError(f"Document with id {document_id} has been modified or does not exist with version {expected_version}.")
        raise
