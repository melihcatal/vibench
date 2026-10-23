import os
from decimal import Decimal
from database_client import get_dynamodb_resource

def conditional_update(document_id: str, table_name: str, updates: dict, key_field: str = "id", expected_version_field: str = None, expected_version_value: int = None, region_name: str = None):
    region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
    dynamodb = get_dynamodb_resource(region_name=region_name)
    table = dynamodb.Table(table_name)

    update_expression_parts = []
    expression_attribute_values = {}
    expression_attribute_names = {}
    
    for k, v in updates.items():
        # DynamoDB does not allow dots in attribute names for ExpressionAttributeNames. Replace with placeholder.
        attr_name_placeholder = f"#attr_{k.replace('.', '_')}"
        update_expression_parts.append(f"{attr_name_placeholder} = :{k}")
        expression_attribute_values[f":{k}"] = v
        expression_attribute_names[attr_name_placeholder] = k

    update_expression = "SET " + ", ".join(update_expression_parts)

    condition_expression = None
    if expected_version_field and expected_version_value is not None:
        # Ensure the version field is also properly named in the expression
        version_attr_name_placeholder = f"#attr_{expected_version_field.replace('.', '_')}"
        condition_expression = f"{version_attr_name_placeholder} = :expected_version_val"
        expression_attribute_values[":expected_version_val"] = expected_version_value
        expression_attribute_names[version_attr_name_placeholder] = expected_version_field

    update_kwargs = {
        "Key": {key_field: document_id},
        "UpdateExpression": update_expression,
        "ExpressionAttributeValues": expression_attribute_values,
        "ReturnValues": "UPDATED_NEW"
    }
    
    if expression_attribute_names:
        update_kwargs["ExpressionAttributeNames"] = expression_attribute_names

    if condition_expression:
        update_kwargs["ConditionExpression"] = condition_expression

    try:
        response = table.update_item(**update_kwargs)
        return response.get("Attributes")
    except Exception as e:
        print(f"Conditional update failed: {e}")
        return None
