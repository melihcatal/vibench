import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError


def conditional_update(table_name: str, document_id: str, new_content: str, expected_version: int) -> Dict[str, Any]:
    dynamodb = boto3.resource("dynamodb", region_name=os.environ.get("AWS_REGION"))
    table = dynamodb.Table(table_name)
    try:
        response = table.update_item(
            Key={"document_id": document_id},
            UpdateExpression="SET content = :content, version = version + :inc",
            ConditionExpression="version = :expected_version",
            ExpressionAttributeValues={
                ":content": new_content,
                ":inc": 1,
                ":expected_version": expected_version,
            },
            ReturnValues="ALL_NEW",
        )
        return {"ok": True, "item": response.get("Attributes", {})}
    except ClientError as exc:
        if exc.response.get("Error", {}).get("Code") == "ConditionalCheckFailedException":
            return {"ok": False, "error": "version_mismatch"}
        raise


def main() -> None:
    table_name = os.environ["DYNAMODB_TABLE_NAME"]
    document_id = os.environ["DOCUMENT_ID"]
    new_content = os.environ["NEW_CONTENT"]
    expected_version = int(os.environ["EXPECTED_VERSION"])
    result = conditional_update(table_name, document_id, new_content, expected_version)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
