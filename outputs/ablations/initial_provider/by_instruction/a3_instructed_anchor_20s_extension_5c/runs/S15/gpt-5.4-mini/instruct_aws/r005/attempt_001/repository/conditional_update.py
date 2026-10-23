from boto3.dynamodb.conditions import Attr

from database_client import dynamodb_table
from database_models import document_key


def conditional_update(document_id, updates, expected_version):
    table = dynamodb_table()
    expr_names = {}
    expr_values = {":expected_version": int(expected_version)}
    set_parts = []
    for index, (key, value) in enumerate(updates.items()):
        name_key = f"#n{index}"
        value_key = f":v{index}"
        expr_names[name_key] = key
        expr_values[value_key] = value
        set_parts.append(f"{name_key} = {value_key}")
    expr_values[":next_version"] = int(expected_version) + 1
    update_expression = "SET " + ", ".join(set_parts + ["version = :next_version"]) if set_parts else "SET version = :next_version"
    table.update_item(
        Key=document_key(document_id),
        UpdateExpression=update_expression,
        ConditionExpression=Attr("version").eq(int(expected_version)) | Attr("version").not_exists(),
        ExpressionAttributeNames=expr_names if expr_names else None,
        ExpressionAttributeValues=expr_values,
    )
    return {"document_id": str(document_id), "version": int(expected_version) + 1, "updated_fields": dict(updates)}


def handler(event, context=None):
    return conditional_update(event["document_id"], event.get("updates", {}), event["expected_version"])
