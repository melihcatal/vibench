from boto3.dynamodb.conditions import Attr

from database_client import dynamodb_table
from database_models import upsert_request


def upsert_document(document_id, payload, version=None):
    table = dynamodb_table()
    item = upsert_request(document_id, payload, version=version)
    condition = None
    if version is not None:
        condition = Attr("version").eq(int(version) - 1) | Attr("version").not_exists()
    params = {"Item": item}
    if condition is not None:
        params["ConditionExpression"] = condition
    table.put_item(**params)
    return item


def handler(event, context=None):
    return upsert_document(event["document_id"], event.get("payload", {}), event.get("version"))
