import os
import json
import boto3
from botocore.exceptions import ClientError
from database_client import get_dynamodb_client, get_table_name
from database_models import ConditionalUpdateRequest, ConditionalUpdateResponse


def conditional_update(request: ConditionalUpdateRequest) -> ConditionalUpdateResponse:
    """
    Applies a conditional or version-aware update to one stored document in DynamoDB.
    """
    dynamodb = get_dynamodb_client()
    table_name = get_table_name()

    try:
        # Build update expression
        update_expression = "SET "
        expression_attribute_names = {}
        expression_attribute_values = {}

        update_parts = []
        for i, (field, value) in enumerate(request.updates.items()):
            field_alias = f"#f{i}"
            value_alias = f":v{i}"

            update_parts.append(f"{field_alias} = {value_alias}")
            expression_attribute_names[field_alias] = field
            expression_attribute_values[value_alias] = {"S": str(value)}

        update_expression += ", ".join(update_parts)

        # Add updated_at timestamp
        if "updated_at" not in request.updates:
            update_expression += ", #updated_at = :updated_at_val"
            expression_attribute_names["#updated_at"] = "updated_at"
            expression_attribute_values[":updated_at_val"] = {
                "S": str(request.timestamp)
            }

        # Build condition expression
        condition_expression_parts = []

        if request.version_condition:
            # Version-based condition (optimistic locking)
            condition_expression_parts.append("attribute_exists(#id)")
            if request.version_condition.get("field"):
                version_field = request.version_condition["field"]
                expected_version = request.version_condition["expected_value"]
                condition_expression_parts.append(
                    f"#{version_field} = :expected_version"
                )
                expression_attribute_names[f"#{version_field}"] = version_field
                expression_attribute_values[":expected_version"] = {
                    "S": str(expected_version)
                }

        elif request.condition_expression:
            # Custom condition expression
            condition_expression_parts.append(request.condition_expression)
            if request.expression_attribute_names:
                expression_attribute_names.update(request.expression_attribute_names)
            if request.expression_attribute_values:
                for key, value in request.expression_attribute_values.items():
                    if isinstance(value, str):
                        expression_attribute_values[key] = {"S": value}
                    elif isinstance(value, (int, float)):
                        expression_attribute_values[key] = {"N": str(value)}
                    elif isinstance(value, bool):
                        expression_attribute_values[key] = {"BOOL": value}
                    elif value is None:
                        expression_attribute_values[key] = {"NULL": True}
                    else:
                        expression_attribute_values[key] = {"S": json.dumps(value)}

        else:
            # Default condition: document must exist
            condition_expression_parts.append("attribute_exists(#id)")

        condition_expression = " AND ".join(condition_expression_parts)
        expression_attribute_names["#id"] = "id"

        # Execute update
        response = dynamodb.update_item(
            TableName=table_name,
            Key={"id": {"S": request.document_id}},
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW",  # Return the updated item
        )

        # Check if update was successful
        if "Attributes" in response:
            # Convert returned attributes
            attributes = response["Attributes"]
            updated_data = {}

            for key, value in attributes.items():
                if "S" in value:
                    try:
                        updated_data[key] = json.loads(value["S"])
                    except json.JSONDecodeError:
                        updated_data[key] = value["S"]
                elif "N" in value:
                    num_str = value["N"]
                    try:
                        updated_data[key] = int(num_str)
                    except ValueError:
                        try:
                            updated_data[key] = float(num_str)
                        except ValueError:
                            updated_data[key] = num_str
                elif "BOOL" in value:
                    updated_data[key] = value["BOOL"]
                elif "M" in value:
                    updated_data[key] = value["M"]
                elif "L" in value:
                    updated_data[key] = value["L"]
                elif "NULL" in value:
                    updated_data[key] = None

            return ConditionalUpdateResponse(
                success=True,
                document_id=request.document_id,
                was_updated=True,
                updated_document=updated_data.get("data", {}),
                metadata={
                    "updated_at": updated_data.get("updated_at"),
                    "version": updated_data.get("version"),
                    "full_item": updated_data,
                },
                timestamp=request.timestamp,
            )
        else:
            return ConditionalUpdateResponse(
                success=False,
                document_id=request.document_id,
                was_updated=False,
                error="Update succeeded but no attributes returned",
                timestamp=request.timestamp,
            )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]

        if error_code == "ConditionalCheckFailedException":
            return ConditionalUpdateResponse(
                success=False,
                document_id=request.document_id,
                was_updated=False,
                condition_failed=True,
                error=f"Condition check failed: {error_message}",
                timestamp=request.timestamp,
            )
        else:
            return ConditionalUpdateResponse(
                success=False,
                document_id=request.document_id,
                was_updated=False,
                error=f"DynamoDB {error_code}: {error_message}",
                timestamp=request.timestamp,
            )
    except Exception as e:
        return ConditionalUpdateResponse(
            success=False,
            document_id=request.document_id,
            was_updated=False,
            error=f"Unexpected error: {str(e)}",
            timestamp=request.timestamp,
        )
