import os
import boto3
from database_client import get_dynamodb_client
from database_models import DocumentQueryRequest, DocumentQueryResponse


class QueryDocuments:
    def __init__(self):
        # DynamoDB region; uses AWS credentials from environment
        self.dynamodb = get_dynamodb_client()

    def query(self, request: DocumentQueryRequest) -> DocumentQueryResponse:
        """Query DynamoDB for documents matching a field value or partition key.

        Uses boto3 (AWS SDK) with DynamoDB as the concrete NoSQL store.
        """
        table_name = os.getenv("DYNAMODB_TABLE")
        if not table_name:
            raise RuntimeError("DYNAMODB_TABLE env var not set")

        table = self.dynamodb.Table(table_name)
        # Simple filter expression for demonstration
        key_condition = {
            "ExpressionAttributeNames": {"#PK": "id"},
            "ExpressionAttributeValues": {":val": request.value},
            "FilterExpression": "#PK = :val",
        }
        response = table.scan(
            FilterExpression=key_condition.get("FilterExpression"),
            ExpressionAttributeNames=key_condition.get("ExpressionAttributeNames"),
            ExpressionAttributeValues=key_condition.get("ExpressionAttributeValues"),
        )
        items = response.get("Items", [])
        return DocumentQueryResponse(matches=items)
