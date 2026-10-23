import os
import json
import boto3
from botocore.exceptions import ClientError
from typing import List, Dict, Any, Optional
from database_client import get_dynamodb_client, get_table_name
from database_models import DocumentQueryRequest, DocumentQueryResponse, DocumentRecord


def query_documents(request: DocumentQueryRequest) -> DocumentQueryResponse:
    """
    Queries documents by a field value or partition-style key from DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    table_name = get_table_name()

    try:
        # Build query parameters based on request type
        if request.partition_key and request.sort_key:
            # Query with partition key and sort key condition
            key_condition_expression = "#pk = :pk_val"
            expression_attribute_names = {"#pk": request.partition_key}
            expression_attribute_values = {":pk_val": {"S": str(request.sort_key)}}

            if request.sort_key_condition:
                # Add sort key condition (begins_with, between, etc.)
                if request.sort_key_condition.get("operator") == "begins_with":
                    key_condition_expression += " AND begins_with(#sk, :sk_val)"
                    expression_attribute_names["#sk"] = request.sort_key
                    expression_attribute_values[":sk_val"] = {
                        "S": str(request.sort_key_condition.get("value"))
                    }

            response = dynamodb.query(
                TableName=table_name,
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                Limit=request.limit or 100,
                ScanIndexForward=request.scan_index_forward
                if request.scan_index_forward is not None
                else True,
            )

        elif request.field_name and request.field_value:
            # Use filter expression for non-key field queries
            # Note: This will scan if no GSI is available
            filter_expression = "#field = :field_val"
            expression_attribute_names = {"#field": request.field_name}
            expression_attribute_values = {
                ":field_val": {"S": str(request.field_value)}
            }

            response = dynamodb.scan(
                TableName=table_name,
                FilterExpression=filter_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                Limit=request.limit or 100,
            )

        else:
            # Simple scan with optional filter
            scan_params = {"TableName": table_name, "Limit": request.limit or 100}

            if request.filter_expression:
                scan_params["FilterExpression"] = request.filter_expression
                if request.expression_attribute_names:
                    scan_params["ExpressionAttributeNames"] = (
                        request.expression_attribute_names
                    )
                if request.expression_attribute_values:
                    # Convert values to DynamoDB format
                    converted_values = {}
                    for key, value in request.expression_attribute_values.items():
                        if isinstance(value, str):
                            converted_values[key] = {"S": value}
                        elif isinstance(value, (int, float)):
                            converted_values[key] = {"N": str(value)}
                        elif isinstance(value, bool):
                            converted_values[key] = {"BOOL": value}
                        elif value is None:
                            converted_values[key] = {"NULL": True}
                        else:
                            converted_values[key] = {"S": json.dumps(value)}
                    scan_params["ExpressionAttributeValues"] = converted_values

            response = dynamodb.scan(**scan_params)

        # Process items
        documents = []
        for item in response.get("Items", []):
            # Convert DynamoDB item to regular Python dict
            document_data = {}
            for key, value in item.items():
                if "S" in value:
                    try:
                        document_data[key] = json.loads(value["S"])
                    except json.JSONDecodeError:
                        document_data[key] = value["S"]
                elif "N" in value:
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

            # Extract document ID and data
            doc_id = document_data.get("id", "unknown")
            data = document_data.get("data", {})

            documents.append(
                DocumentRecord(
                    document_id=doc_id,
                    document_data=data,
                    metadata={
                        "created_at": document_data.get("created_at"),
                        "updated_at": document_data.get("updated_at"),
                        "full_item": document_data,
                    },
                )
            )

        # Check for pagination
        last_evaluated_key = response.get("LastEvaluatedKey")
        has_more = last_evaluated_key is not None

        return DocumentQueryResponse(
            success=True,
            documents=documents,
            count=len(documents),
            has_more=has_more,
            last_evaluated_key=last_evaluated_key,
            timestamp=request.timestamp,
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        return DocumentQueryResponse(
            success=False,
            documents=[],
            count=0,
            error=f"DynamoDB {error_code}: {error_message}",
            timestamp=request.timestamp,
        )
    except Exception as e:
        return DocumentQueryResponse(
            success=False,
            documents=[],
            count=0,
            error=f"Unexpected error: {str(e)}",
            timestamp=request.timestamp,
        )
