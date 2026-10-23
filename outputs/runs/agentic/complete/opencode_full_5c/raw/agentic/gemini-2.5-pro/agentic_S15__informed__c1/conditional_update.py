from botocore.exceptions import ClientError
from database_client import get_db_table
from database_models import DocumentUpdate


def conditional_update(
    document_id: str, update_data: DocumentUpdate, expected_version: int
):
    """
    Applies a conditional update to a document if the version matches.

    :param document_id: The ID of the document to update.
    :param update_data: A dictionary with the fields to update.
    :param expected_version: The version number the document is expected to have.
    :return: The updated attributes or an error dictionary.
    """
    table = get_db_table()

    update_expression_parts = []
    expression_attribute_values = {
        ":new_version": expected_version + 1,
        ":expected_version": expected_version,
    }
    expression_attribute_names = {"#v": "version"}

    # Set version update
    update_expression_parts.append("#v = :new_version")

    # Add other fields to update
    for key, value in update_data.items():
        if value is not None:
            placeholder = f":{key}"
            nameholder = f"#{key}"
            update_expression_parts.append(f"{nameholder} = {placeholder}")
            expression_attribute_values[placeholder] = value
            expression_attribute_names[nameholder] = key

    update_expression = "SET " + ", ".join(update_expression_parts)

    try:
        response = table.update_item(
            Key={"document_id": document_id},
            UpdateExpression=update_expression,
            ConditionExpression="#v = :expected_version",
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="UPDATED_NEW",
        )
        return response["Attributes"]
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {"error": "Conditional check failed: version mismatch."}
        else:
            raise e
