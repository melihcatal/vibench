from database_client import get_db_table
from boto3.dynamodb.conditions import Attr
from typing import Dict, Any
from botocore.exceptions import ClientError


def update_document_content_if_version_matches(
    doc_id: str, new_content: str, expected_version: int
) -> Dict[str, Any]:
    table = get_db_table()
    new_version = expected_version + 1

    try:
        response = table.update_item(
            Key={"doc_id": doc_id},
            UpdateExpression="set content = :c, #v = :v_new",
            ConditionExpression=Attr("version").eq(expected_version),
            ExpressionAttributeNames={"#v": "version"},
            ExpressionAttributeValues={
                ":c": new_content,
                ":v_new": new_version,
            },
            ReturnValues="UPDATED_NEW",
        )
        return response
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            # Handle the conditional check failure gracefully
            print(f"Conditional update failed for doc_id {doc_id}: Version mismatch.")
            return {"error": "ConditionalCheckFailedException", "message": str(e)}
        else:
            raise
