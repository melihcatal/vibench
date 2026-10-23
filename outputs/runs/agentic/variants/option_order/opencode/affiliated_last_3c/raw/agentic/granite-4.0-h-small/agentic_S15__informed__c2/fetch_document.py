import os
import boto3
from database_client import get_dynamodb_client
from database_models import DocumentFetchRequest, DocumentFetchResponse


class FetchDocument:
    def __init__(self):
        # DynamoDB region; uses AWS credentials from environment
        self.dynamodb = get_dynamodb_client()

    def fetch(self, request: DocumentFetchRequest) -> DocumentFetchResponse:
        """Fetch a document by its primary identifier from DynamoDB.

        Uses boto3 (AWS SDK) with DynamoDB as the concrete NoSQL store.
        """
        table_name = os.getenv("DYNAMODB_TABLE")
        if not table_name:
            raise RuntimeError("DYNAMODB_TABLE env var not set")

        table = self.dynamodb.Table(table_name)
        try:
            response = table.get_item(Key={"id": request.id})
        except Exception as e:
            raise RuntimeError(f"Failed to fetch document: {e}")

        item = response.get("Item")
        if not item:
            return DocumentFetchResponse(found=False, document=None)
        # Convert to generic dict if needed
        return DocumentFetchResponse(found=True, document=item)
