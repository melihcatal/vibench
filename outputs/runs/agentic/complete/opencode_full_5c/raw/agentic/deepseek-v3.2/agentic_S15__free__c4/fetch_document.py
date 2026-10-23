import boto3
from botocore.exceptions import ClientError
import os
from database_client import get_dynamodb_client
from database_models import DocumentFetchRequest, DocumentFetchResponse


def fetch_document(request: DocumentFetchRequest) -> DocumentFetchResponse:
    """
    Fetches a document by identifier from DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    table_name = os.environ.get("DYNAMODB_TABLE", "documents")

    try:
        response = dynamodb.get_item(
            TableName=table_name, Key={"id": {"S": request.document_id}}
        )

        item = response.get("Item")
        if item:
            document = {
                key: value.get("S")
                or value.get("N")
                or value.get("BOOL")
                or json.loads(value.get("S", "{}"))
                for key, value in item.items()
            }
            return DocumentFetchResponse(
                success=True,
                document_id=request.document_id,
                document=document,
                message=f"Document {request.document_id} fetched successfully",
            )
        else:
            return DocumentFetchResponse(
                success=False,
                document_id=request.document_id,
                error_message="Document not found",
                message=f"Document {request.document_id} not found",
            )
    except ClientError as e:
        return DocumentFetchResponse(
            success=False,
            document_id=request.document_id,
            error_message=str(e),
            message=f"Failed to fetch document {request.document_id}",
        )
