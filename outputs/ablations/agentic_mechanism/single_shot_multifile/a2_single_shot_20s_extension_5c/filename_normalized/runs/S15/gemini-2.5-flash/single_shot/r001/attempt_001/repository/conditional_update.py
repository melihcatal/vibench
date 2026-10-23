import os
from typing import Dict, Any, Optional
from database_client import get_dynamodb_client, get_table_name, serialize_item, deserialize_item
from database_models import ConditionalUpdateRequest, Document
import boto3

def conditional_update(request: ConditionalUpdateRequest) -> Optional[Document]:
    """
    Applies a conditional or version-aware update to one stored document in AWS DynamoDB.
    Updates the document only if its current version matches the expected_version.
    Automatically increments the version on successful update.
    """
    dynamodb = get_dynamodb_client()
    table_name = get_table_name()

    key_item = {"id": request.id}
    dynamodb_key = serialize_item(key_item)

    update_expression_parts = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    for k, v in request.updates.items():
        attr_name_key = f"#{k}"
        attr_value_key = f":{k}"
        update_expression_parts.append(f"{attr_name_key} = {attr_value_key}")
        expression_attribute_names[attr_name_key] = k
        expression_attribute_values[attr_value_key] = serialize_item({"v": v})["v"]

    update_expression_parts.append("#version_attr = :new_version_val")
    expression_attribute_names["#version_attr"] = "version"
    expression_attribute_values[":new_version_val"] = serialize_item({"v": request.expected_version + 1})["v"]

    update_expression = "SET " + ", ".join(update_expression_parts)

    condition_expression = "#version_attr = :expected_version_val"
    expression_attribute_values[":expected_version_val"] = serialize_item({"v": request.expected_version})["v"]
    expression_attribute_names["#version_attr"] = "version"

    try:
        response = dynamodb.update_item(
            TableName=table_name,
            Key=dynamodb_key,
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )
        updated_item = response.get("Attributes")
        if updated_item:
            return Document(**deserialize_item(updated_item))
        return None
    except boto3.client("dynamodb").exceptions.ConditionalCheckFailedException:
        print(f"Conditional check failed: document {request.id} version was not {request.expected_version}")
        return None
    except Exception as e:
        print(f"Error updating document: {e}")
        raise
