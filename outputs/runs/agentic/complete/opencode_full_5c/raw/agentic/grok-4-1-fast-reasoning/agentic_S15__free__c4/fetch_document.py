import boto3
from database_client import DYNAMODB_TABLE_NAME, AWS_REGION
from database_models import FetchResponse, Document


def fetch_document(doc_id: str) -> FetchResponse:
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    resp = table.get_item(Key={"id": doc_id})
    return resp.get("Item")
