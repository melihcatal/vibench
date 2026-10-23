import boto3
from botocore.exceptions import ClientError
import json
import os
from database_client import get_dynamodb_client
from database_models import ConditionalUpdateRequest, ConditionalUpdateResponse


def conditional_update(request: ConditionalUpdateRequest) -> ConditionalUpdateResponse:
    """
    Applies a conditional or version-aware update to one stored document in DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    table_name = os.environ.get("DYNAMODB_TABLE", "documents")

    try:
        update_expression = "SET "
        expression_values = {}
        expression_names = {}

        for i, (key, value) in enumerate(request.updates.items()):
            placeholder = f":val{i}"
            name_placeholder = f"#attr{i}"
            update_expression += f"{name_placeholder} = {placeholder}, "
            expression_values[placeholder] = (
                {"S": str(value)}
                if isinstance(value, str)
                else {"N": str(value)}
                if isinstance(value, (int, float))
                else {"BOOL": value}
                if isinstance(value, bool)
                else {"S": json.dumps(value)}
            )
            expression_names[name_placeholder] = key

        update_expression = update_expression.rstrip(", ")

        condition_expression = None
        if request.condition_field and request.condition_value:
            condition_expression = (
                f"attribute_exists(id) AND {request.condition_field} = :cond"
            )
            expression_values[":cond"] = {"S": str(request.condition_value)}
        elif request.version_field:
            condition_expression = (
                f"attribute_exists(id) AND {request.version_field} = :version"
            )
            expression_values[":version"] = {"N": str(request.expected_version)}

        response = dynamodb.update_item(
            TableName=table_name,
            Key={"id": {"S": request.document_id}},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names if expression_names else None,
            ConditionExpression=condition_expression,
            ReturnValues="ALL_NEW",
        )

        updated_document = {
            key: value.get("S")
            or value.get("N")
            or value.get("BOOL")
            or json.loads(value.get("S", "{}"))
            for key, value in response.get("Attributes", {}).items()
        }

        return ConditionalUpdateResponse(
            success=True,
            document_id=request.document_id,
            updated_document=updated_document,
            message=f"Document {request.document_id} updated successfully with condition",
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return ConditionalUpdateResponse(
                success=False,
                document_id=request.document_id,
                error_message="Condition check failed",
                message=f"Condition check failed for document {request.document_id}",
            )
        else:
            return ConditionalUpdateResponse(
                success=False,
                document_id=request.document_id,
                error_message=str(e),
                message=f"Failed to update document {request.document_id}",
            )
