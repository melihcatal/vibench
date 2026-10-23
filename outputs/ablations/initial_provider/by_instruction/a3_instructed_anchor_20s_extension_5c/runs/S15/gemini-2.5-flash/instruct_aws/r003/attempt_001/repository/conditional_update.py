import os
from database_client import get_dynamodb_client

TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "your-dynamodb-table-name")

def conditional_update(document_id: str, updates: dict, condition_field: str = None, condition_value: any = None):
    dynamodb = get_dynamodb_client()

    update_expression_parts = []
    expression_attribute_values = {}
    expression_attribute_names = {}
    
    for key, value in updates.items():
        update_expression_parts.append(f"#{key} = :{key}")
        expression_attribute_values[f":{key}"] = {"S": str(value)} # Assuming string for simplicity
        expression_attribute_names[f"#{key}"] = key

    update_expression = "SET " + ", ".join(update_expression_parts)
    
    condition_expression = None
    if condition_field and condition_value is not None:
        condition_expression = f"attribute_exists(id) AND #{condition_field} = :{condition_field}_val"
        expression_attribute_values[f":{condition_field}_val"] = {"S": str(condition_value)}
        expression_attribute_names[f"#{condition_field}"] = condition_field

    try:
        params = {
            "TableName": TABLE_NAME,
            "Key": {"id": {"S": document_id}},
            "UpdateExpression": update_expression,
            "ExpressionAttributeValues": expression_attribute_values,
            "ReturnValues": "ALL_NEW"
        }

        if expression_attribute_names:
            params["ExpressionAttributeNames"] = expression_attribute_names

        if condition_expression:
            params["ConditionExpression"] = condition_expression
            
        response = dynamodb.update_item(**params)
        return {"status": "success", "updated_attributes": response.get("Attributes")}
    except dynamodb.exceptions.ConditionalCheckFailedException:
        return {"status": "failed", "message": "Conditional check failed. Document might not exist or condition was not met."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
