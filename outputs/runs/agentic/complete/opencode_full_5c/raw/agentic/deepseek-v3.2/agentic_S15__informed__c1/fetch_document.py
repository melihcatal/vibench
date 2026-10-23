import os
import json
import boto3
from botocore.exceptions import ClientError
from database_client import get_dynamodb_client, get_table_name
from database_models import DocumentFetchRequest, DocumentFetchResponse


def fetch_document(request: DocumentFetchRequest) -> DocumentFetchResponse:
    """
    Fetches a document by identifier from DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    table_name = get_table_name()

    try:
        # Use get_item to fetch the document by primary key
        response = dynamodb.get_item(
            TableName=table_name,
            Key={"id": {"S": request.document_id}},
            ConsistentRead=request.consistent_read or False,
        )

        # Check if item was found
        if "Item" not in response:
            return DocumentFetchResponse(
                success=False,
                document_id=request.document_id,
                found=False,
                error="Document not found",
                timestamp=request.timestamp,
            )

        # Convert DynamoDB item to regular Python dict
        item = response["Item"]
        document_data = {}

        for key, value in item.items():
            if "S" in value:
                # Try to parse JSON strings, otherwise keep as string
                try:
                    document_data[key] = json.loads(value["S"])
                except json.JSONDecodeError:
                    document_data[key] = value["S"]
            elif "N" in value:
                # Try to parse as int, then float
                num_str = value["N"]
                try:
                    document_data[key] = int(num_str)
                except ValueError:
                    try:
                        document_data[key] = float(num_str)
                    except ValueError:
                        document_data[key] = num_str
            elif "BOOL" in value:
                document_data[key] = value["BOOL"]
            elif "M" in value:
                document_data[key] = value["M"]
            elif "L" in value:
                document_data[key] = value["L"]
            elif "NULL" in value:
                document_data[key] = None

        # Extract the main data field
        data = document_data.get("data", {})

        return DocumentFetchResponse(
            success=True,
            document_id=request.document_id,
            found=True,
            document_data=data,
            metadata={
                "created_at": document_data.get("created_at"),
                "updated_at": document_data.get("updated_at"),
                "full_item": document_data,
            },
            timestamp=request.timestamp,
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        return DocumentFetchResponse(
            success=False,
            document_id=request.document_id,
            found=False,
            error=f"DynamoDB {error_code}: {error_message}",
            timestamp=request.timestamp,
        )
    except Exception as e:
        return DocumentFetchResponse(
            success=False,
            document_id=request.document_id,
            found=False,
            error=f"Unexpected error: {str(e)}",
            timestamp=request.timestamp,
        )
