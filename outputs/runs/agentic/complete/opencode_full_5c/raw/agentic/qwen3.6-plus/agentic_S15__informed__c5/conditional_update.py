from boto3.dynamodb.conditions import Attr
from database_client import get_table, serialize_item
from database_models import UpdateResult, DocumentResponse


def conditional_update(
    document_id,
    update_fields,
    expected_version=None,
    table_name=None,
    partition_key="document_id",
):
    table = get_table(table_name)

    update_expr_parts = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    for idx, (field_name, field_value) in enumerate(update_fields.items()):
        placeholder_name = f"#f{idx}"
        placeholder_value = f":v{idx}"
        update_expr_parts.append(f"{placeholder_name} = {placeholder_value}")
        expression_attribute_names[placeholder_name] = field_name
        expression_attribute_values[placeholder_value] = field_value

    update_expression = "SET " + ", ".join(update_expr_parts)

    condition_expr = None
    if expected_version is not None:
        condition_expr = Attr("version").eq(expected_version)

    key = {partition_key: document_id}

    kwargs = {
        "Key": key,
        "UpdateExpression": update_expression,
        "ExpressionAttributeValues": expression_attribute_values,
        "ExpressionAttributeNames": expression_attribute_names,
        "ReturnValues": "ALL_NEW",
    }
    if condition_expr is not None:
        kwargs["ConditionExpression"] = condition_expr

    try:
        response = table.update_item(**kwargs)
        updated_item = response.get("Attributes", {})
        new_version = updated_item.get("version", expected_version)
        if new_version is None or expected_version is None:
            new_version = (expected_version or 0) + 1
        else:
            new_version = expected_version + 1

        updated_item["version"] = new_version
        table.update_item(
            Key=key,
            UpdateExpression="SET #ver = :nv",
            ExpressionAttributeNames={"#ver": "version"},
            ExpressionAttributeValues={":nv": new_version},
        )

        return UpdateResult(
            document_id=document_id,
            success=True,
            version=new_version,
        )
    except Exception as exc:
        error_str = str(exc)
        if "ConditionalCheckFailedException" in error_str:
            return UpdateResult(
                document_id=document_id,
                success=False,
                condition_check_failed=True,
                error="Condition check failed: version mismatch or condition not met",
            )
        return UpdateResult(
            document_id=document_id,
            success=False,
            error=error_str,
        )
