import os
import boto3
from database_client import get_dynamodb_client
from database_models import (
    DocumentConditionalUpdateRequest,
    DocumentConditionalUpdateResponse,
)


class ConditionalUpdate:
    def __init__(self):
        # DynamoDB region; uses AWS credentials from environment
        self.dynamodb = get_dynamodb_client()

    def update(
        self, request: DocumentConditionalUpdateRequest
    ) -> DocumentConditionalUpdateResponse:
        """Apply a conditional (version-aware) update to a DynamoDB document.

        Uses boto3 (AWS SDK) with DynamoDB as the concrete NoSQL store.
        Checks the document's version attribute before updating.
        """
        table_name = os.getenv("DYNAMODB_TABLE")
        if not table_name:
            raise RuntimeError("DYNAMODB_TABLE env var not set")

        table = self.dynamodb.Table(table_name)
        key = {"id": request.id}
        # Assume document has a version attribute for condition
        condition = "attribute_exists(version) and version = :ver"
        expression_values = {":ver": request.expected_version}
        update_expr = "set data = :new_data"
        expression_attributes = {":new_data": request.new_data}
        try:
            response = table.update_item(
                Key=key,
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expression_values,
                ConditionExpression=condition,
                ExpressionAttributeNames={"#D": "data"},
                ReturnValues="ALL_NEW",
            )
        except self.dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
            return DocumentConditionalUpdateResponse(
                success=False, message="Conditional check failed - version mismatch"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to perform conditional update: {e}")

        updated_doc = response.get("Attributes")
        return DocumentConditionalUpdateResponse(
            success=True,
            message="Conditional update succeeded",
            updated_document=updated_doc,
        )
