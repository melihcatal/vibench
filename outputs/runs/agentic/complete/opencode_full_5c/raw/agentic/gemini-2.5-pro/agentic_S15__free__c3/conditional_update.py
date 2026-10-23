from botocore.exceptions import ClientError
from database_client import get_database_client, get_table_name
from database_models import DocumentUpdate


def conditional_update(
    document_id: str, updates: DocumentUpdate, expected_version: int
):
    """
    Applies a conditional update to a document in DynamoDB.
    The update will only succeed if the document's version matches the expected_version.
    """
    dynamodb = get_database_client()
    table = dynamodb.Table(get_table_name())

    update_expression_parts = []
    expression_attribute_values = {
        ":expected_version": expected_version,
        ":new_version": expected_version + 1,
    }
    expression_attribute_names = {"#v": "version"}

    if updates.get("content"):
        update_expression_parts.append("#c = :content")
        expression_attribute_names["#c"] = "content"
        expression_attribute_values[":content"] = updates["content"]

    if updates.get("author"):
        update_expression_parts.append("#a = :author")
        expression_attribute_names["#a"] = "author"
        expression_attribute_values[":author"] = updates["author"]

    if not update_expression_parts:
        return {"status": "no_op", "message": "No update fields provided."}

    update_expression_parts.append("#v = :new_version")
    update_expression = "SET " + ", ".join(update_expression_parts)
    condition_expression = "#v = :expected_version"

    try:
        response = table.update_item(
            Key={"document_id": document_id},
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW",
        )
        return {"status": "success", "attributes": response.get("Attributes")}
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {
                "status": "error",
                "message": "Version mismatch. The document has been updated by another process.",
            }
        else:
            return {"status": "error", "message": e.response["Error"]["Message"]}
