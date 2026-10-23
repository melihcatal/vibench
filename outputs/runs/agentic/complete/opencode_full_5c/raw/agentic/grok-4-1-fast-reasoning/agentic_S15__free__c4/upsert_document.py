import boto3
from database_client import DYNAMODB_TABLE_NAME, AWS_REGION
from database_models import Document, UpsertResponse


def upsert_document(doc_id: str, document: Document) -> UpsertResponse:
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    item = {"id": doc_id, **document}
    if "version" not in item:
        item["version"] = 1
    table.put_item(Item=item)
    return {"status": "success", "doc_id": doc_id}
