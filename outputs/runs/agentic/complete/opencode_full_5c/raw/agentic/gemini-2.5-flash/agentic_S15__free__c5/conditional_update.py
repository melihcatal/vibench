from database_client import get_dynamodb_client
from database_models import Document
import os


def conditional_update_document(
    document_id: str, updates: dict, condition_field: str, expected_value: str
):
    """
    Applies a conditional or version-aware update to one stored document in AWS DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    table_name = os.environ.get(
        "DYNAMODB_TABLE_NAME", "your-document-table"
    )  # AWS DynamoDB

    update_expression_parts = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    for i, (key, value) in enumerate(updates.items()):
        attr_name_placeholder = f"#attr{i}"
        attr_value_placeholder = f":val{i}"
        update_expression_parts.append(
            f"{attr_name_placeholder} = {attr_value_placeholder}"
        )
        expression_attribute_values[attr_value_placeholder] = {
            "S": str(value)
        }  # Assuming string for simplicity
        expression_attribute_names[attr_name_placeholder] = key

    update_expression = "SET " + ", ".join(update_expression_parts)

    # Add condition expression
    condition_expression = f"#cond_field = :expected_val"
    expression_attribute_values[":expected_val"] = {"S": expected_value}
    expression_attribute_names["#cond_field"] = condition_field

    try:
        response = dynamodb.update_item(
            TableName=table_name,
            Key={"id": {"S": document_id}},
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,  # AWS DynamoDB
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="UPDATED_NEW",
        )
        return response
    except dynamodb.exceptions.ConditionalCheckFailedException:
        print(
            f"Conditional check failed for document {document_id}. Field '{condition_field}' did not have expected value '{expected_value}'."
        )
        return None
