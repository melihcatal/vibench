import os

from boto3.dynamodb.conditions import Attr

from database_client import get_table
from database_models import build_status_response, normalize_document


def conditional_update(
    document_id, updates, expected_version=None, table_name=None, key_name="id"
):
    table = get_table(table_name)
    update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in updates)
    names = {f"#{k}": k for k in updates}
    values = {f":{k}": v for k, v in normalize_document(updates).items()}
    condition = Attr(key_name).eq(document_id)
    if expected_version is not None:
        condition = condition & Attr("version").eq(expected_version)
    response = table.update_item(
        Key={key_name: document_id},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=names,
        ExpressionAttributeValues=values,
        ConditionExpression=condition,
        ReturnValues="ALL_NEW",
    )
    return build_status_response(True, data=response.get("Attributes"))


def main():
    return conditional_update(os.environ["DOCUMENT_ID"], {})
