import os
import boto3
from database_client import get_dynamodb_client
from database_models import DocumentUpsertRequest, DocumentUpsertResponse


class UpsertDocument:
    def __init__(self):
        # DynamoDB region; uses AWS credentials from environment
        self.dynamodb = get_dynamodb_client()

    def upsert(self, request: DocumentUpsertRequest) -> DocumentUpsertResponse:
        """Upsert a JSON document in DynamoDB using its primary identifier.

        Uses the AWS SDK (boto3) and DynamoDB as the concrete Managed NoSQL store.
        """
        table_name = os.getenv("DYNAMODB_TABLE")
        if not table_name:
            raise RuntimeError("DYNAMODB_TABLE env var not set")

        table = self.dynamodb.Table(table_name)
        # DynamoDB accepts the entire item; merge request data
        response = table.put_item(Item=request.to_dict())
        return DocumentUpsertResponse(success=True, message="Upsert completed")


# Example usage (remove in production)
if __name__ == "__main__":
    req = DocumentUpsertRequest(id="doc_123", data={"name": "example"})
    upsert = UpsertDocument()
    print(upsert.upsert(req).to_dict())
