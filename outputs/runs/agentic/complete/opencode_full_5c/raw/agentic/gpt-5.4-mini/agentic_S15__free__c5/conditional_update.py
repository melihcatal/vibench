import json
import sys

from botocore.exceptions import ClientError

from database_client import get_table
from database_models import normalize_document


def conditional_update(document_id: str, updates: dict, version: int | None = None):
    table = get_table()
    update_data = normalize_document(updates)
    expression_names = {f"#k{idx}": key for idx, key in enumerate(update_data)}
    expression_values = {
        f":v{idx}": value for idx, value in enumerate(update_data.values())
    }
    set_clause = ", ".join(
        f"{name} = {value}" for name, value in zip(expression_names, expression_values)
    )
    update_expression = f"SET {set_clause}"
    condition_expression = None
    if version is not None:
        update_expression += ", version = :next_version"
        expression_values[":next_version"] = version + 1
        expression_values[":current_version"] = version
        condition_expression = "version = :current_version"
    try:
        response = table.update_item(
            Key={"document_id": document_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ConditionExpression=condition_expression,
            ReturnValues="ALL_NEW",
        )
        return response.get("Attributes")
    except ClientError:
        raise


def main() -> None:
    payload = json.loads(sys.stdin.read())
    result = conditional_update(
        payload["document_id"], dict(payload["updates"]), payload.get("version")
    )
    sys.stdout.write(json.dumps(result, default=str))


if __name__ == "__main__":
    main()
