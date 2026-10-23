from typing import Dict, Any
from botocore.exceptions import ClientError
from database_client import get_table


def conditional_update(
    table_name: str, doc_id: str, updates: Dict[str, Any], expected_version: int
) -> bool:
    table = get_table(table_name)
    update_parts = ", ".join(f"#{k} = :v{k}" for k in updates)
    attr_names = {f"#{k}": k for k in updates}
    attr_values = {f":v{k}": v for k, v in updates.items()}
    attr_values[":exp_ver"] = expected_version
    try:
        table.update_item(
            Key={"id": doc_id},
            UpdateExpression=f"SET {update_parts}",
            ExpressionAttributeNames=attr_names,
            ExpressionAttributeValues=attr_values,
            ConditionExpression="version = :exp_ver",
        )
        return True
    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ConditionalCheckFailedException":
            return False
        raise
