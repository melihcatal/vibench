import boto3
from boto3.dynamodb.conditions import Attr
from database_client import DYNAMODB_TABLE_NAME, AWS_REGION
from database_models import Documents


def query_documents(field: str, value: str) -> Documents:
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    resp = table.scan(FilterExpression=Attr(field).eq(value))
    return resp["Items"]
