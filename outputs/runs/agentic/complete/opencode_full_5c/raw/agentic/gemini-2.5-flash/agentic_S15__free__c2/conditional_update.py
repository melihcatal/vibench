from database_client import get_dynamodb_client
from typing import Dict, Any, Optional
import os


def conditional_update(
    document_id: str,
    updates: Dict[str, Any],
    condition_field: str,
    expected_value: Any,
    table_name: str | None = None,
) -> Optional[Dict[str, Any]]:
    """
    Applies a conditional update to a single document in an AWS DynamoDB table.
    The update will only succeed if the `condition_field` in the document matches `expected_value`.

    Args:
        document_id: The primary identifier of the document to update.
        updates: A dictionary of attribute updates (e.g., {'status': 'APPROVED', 'version': 2}).
        condition_field: The field name to check for the condition (e.g., 'status', 'version').
        expected_value: The value the `condition_field` must have for the update to proceed.
        table_name: The name of the DynamoDB table. Defaults to 'DocumentsTable'.

    Returns:
        The updated document attributes if the update was successful, otherwise None.
    """
    if table_name is None:
        table_name = os.getenv("DYNAMODB_TABLE_NAME", "DocumentsTable")

    dynamodb = get_dynamodb_client()

    update_expression_parts = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    # Build UpdateExpression and ExpressionAttributeValues
    for i, (key, value) in enumerate(updates.items()):
        # DynamoDB doesn't allow certain characters in attribute names directly, use #name
        attr_name_placeholder = f"#attr{i}"
        attr_value_placeholder = f":val{i}"

        update_expression_parts.append(
            f"{attr_name_placeholder} = {attr_value_placeholder}"
        )
        expression_attribute_values[attr_value_placeholder] = {
            "S": str(value)
        }  # Simplified to string for now
        expression_attribute_names[attr_name_placeholder] = key

    update_expression = "SET " + ", ".join(update_expression_parts)

    # Condition Expression
    condition_attr_name_placeholder = "#condattr"
    condition_attr_value_placeholder = ":condval"

    condition_expression = (
        f"{condition_attr_name_placeholder} = {condition_attr_value_placeholder}"
    )
    expression_attribute_values[condition_attr_value_placeholder] = {
        "S": str(expected_value)
    }  # Simplified to string
    expression_attribute_names[condition_attr_name_placeholder] = condition_field

    try:
        response = dynamodb.update_item(
            TableName=table_name,
            Key={"id": {"S": document_id}},
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="ALL_NEW",
        )

        # Parse the updated attributes back into a friendly dictionary
        updated_attributes = {}
        if "Attributes" in response:
            for key, value_obj in response["Attributes"].items():
                if "S" in value_obj:
                    updated_attributes[key] = value_obj["S"]
                elif "N" in value_obj:
                    updated_attributes[key] = float(value_obj["N"])
                elif "BOOL" in value_obj:
                    updated_attributes[key] = value_obj["BOOL"]
                elif "L" in value_obj:
                    updated_attributes[key] = [v["S"] for v in value_obj["L"]]

        return updated_attributes

    except dynamodb.exceptions.ConditionalCheckFailedException:
        print(
            f"Conditional check failed: Document {document_id} field '{condition_field}' does not have expected value '{expected_value}'."
        )
        return None
    except Exception as e:
        print(f"An error occurred during conditional update: {e}")
        return None
