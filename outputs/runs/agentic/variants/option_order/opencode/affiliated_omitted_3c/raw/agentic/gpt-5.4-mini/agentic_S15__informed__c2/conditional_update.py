from boto3.dynamodb.conditions import Attr

from database_client import get_table, make_key
from database_models import ConditionalUpdateRequest


def conditional_update(request: ConditionalUpdateRequest):
    table = get_table()
    update_expression = []
    expression_values = {}
    expression_names = {}
    for idx, (key, value) in enumerate(request.updates.items()):
        name = f"#f{idx}"
        token = f":v{idx}"
        expression_names[name] = key
        expression_values[token] = value
        update_expression.append(f"{name} = {token}")
    if request.expected_version is not None:
        expression_names["#version"] = request.version_field
        expression_values[":expected_version"] = request.expected_version
        condition = Attr(request.version_field).eq(request.expected_version)
    else:
        condition = None
    result = table.update_item(
        Key=make_key(request.document_id),
        UpdateExpression="SET " + ", ".join(update_expression),
        ExpressionAttributeNames=expression_names,
        ExpressionAttributeValues=expression_values,
        ConditionExpression=condition,
        ReturnValues="ALL_NEW",
    )
    return result.get("Attributes")
