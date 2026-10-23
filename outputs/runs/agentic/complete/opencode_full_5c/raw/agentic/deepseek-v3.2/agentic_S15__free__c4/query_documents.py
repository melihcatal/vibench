import boto3
from botocore.exceptions import ClientError
import json
import os
from database_client import get_dynamodb_client
from database_models import DocumentQueryRequest, DocumentQueryResponse


def query_documents(request: DocumentQueryRequest) -> DocumentQueryResponse:
    """
    Queries documents by a field value or partition-style key from DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    table_name = os.environ.get("DYNAMODB_TABLE", "documents")

    try:
        if request.partition_key and request.sort_key:
            key_condition = f"{request.partition_key_name} = :pk"
            expression_values = {":pk": {"S": request.partition_key}}

            if request.sort_key:
                key_condition += f" AND {request.sort_key_name} = :sk"
                expression_values[":sk"] = {"S": request.sort_key}

            response = dynamodb.query(
                TableName=table_name,
                KeyConditionExpression=key_condition,
                ExpressionAttributeValues=expression_values,
            )
        elif request.field_name and request.field_value:
            filter_expression = f"{request.field_name} = :val"
            expression_values = {":val": {"S": str(request.field_value)}}

            response = dynamodb.scan(
                TableName=table_name,
                FilterExpression=filter_expression,
                ExpressionAttributeValues=expression_values,
            )
        else:
            return DocumentQueryResponse(
                success=False,
                error_message="Either partition_key/sort_key or field_name/field_value must be provided",
                message="Invalid query parameters",
            )

        items = response.get("Items", [])
        documents = []
        for item in items:
            document = {
                key: value.get("S")
                or value.get("N")
                or value.get("BOOL")
                or json.loads(value.get("S", "{}"))
                for key, value in item.items()
            }
            documents.append(document)

        return DocumentQueryResponse(
            success=True,
            documents=documents,
            count=len(documents),
            message=f"Query returned {len(documents)} documents",
        )
    except ClientError as e:
        return DocumentQueryResponse(
            success=False, error_message=str(e), message="Failed to query documents"
        )
