import boto3
from botocore.exceptions import ClientError
import json
import os
from database_client import get_dynamodb_client
from database_models import DocumentUpsertRequest, DocumentUpsertResponse


def upsert_document(request: DocumentUpsertRequest) -> DocumentUpsertResponse:
    """
    Upserts a JSON document by its primary identifier into DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    table_name = os.environ.get("DYNAMODB_TABLE", "documents")

    try:
        item = request.document.copy()
        item["id"] = request.document_id

        response = dynamodb.put_item(
            TableName=table_name,
            Item={
                key: {"S": str(value)}
                if isinstance(value, str)
                else {"N": str(value)}
                if isinstance(value, (int, float))
                else {"BOOL": value}
                if isinstance(value, bool)
                else {"S": json.dumps(value)}
                for key, value in item.items()
            },
            ReturnValues="ALL_OLD",
        )

        return DocumentUpsertResponse(
            success=True,
            document_id=request.document_id,
            old_document=response.get("Attributes"),
            message=f"Document {request.document_id} upserted successfully",
        )
    except ClientError as e:
        return DocumentUpsertResponse(
            success=False,
            document_id=request.document_id,
            error_message=str(e),
            message=f"Failed to upsert document {request.document_id}",
        )
