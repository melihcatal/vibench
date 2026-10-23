import os
import json
import boto3
from botocore.exceptions import ClientError
from database_client import get_dynamodb_client, get_table_name
from database_models import DocumentUpsertRequest, DocumentUpsertResponse


def upsert_document(request: DocumentUpsertRequest) -> DocumentUpsertResponse:
    """
    Upserts a JSON document by its primary identifier into DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    table_name = get_table_name()

    try:
        # Prepare the item for DynamoDB
        item = {
            "id": request.document_id,
            "data": request.document_data,
            "created_at": request.created_at or request.timestamp,
            "updated_at": request.timestamp,
        }

        # Add any additional fields from the request
        if request.additional_fields:
            item.update(request.additional_fields)

        # Use put_item for upsert (overwrites if exists, creates if not)
        response = dynamodb.put_item(
            TableName=table_name,
            Item={
                k: {"S": str(v)}
                if isinstance(v, str)
                else {"N": str(v)}
                if isinstance(v, (int, float))
                else {"BOOL": v}
                if isinstance(v, bool)
                else {"S": json.dumps(v)}
                for k, v in item.items()
            },
            ReturnValues="ALL_OLD",  # Returns the previous item if it existed
        )

        was_updated = "Attributes" in response and response["Attributes"]

        return DocumentUpsertResponse(
            success=True,
            document_id=request.document_id,
            was_created=not was_updated,
            was_updated=was_updated,
            timestamp=request.timestamp,
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        return DocumentUpsertResponse(
            success=False,
            document_id=request.document_id,
            error=f"DynamoDB {error_code}: {error_message}",
            timestamp=request.timestamp,
        )
    except Exception as e:
        return DocumentUpsertResponse(
            success=False,
            document_id=request.document_id,
            error=f"Unexpected error: {str(e)}",
            timestamp=request.timestamp,
        )
