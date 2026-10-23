import json
import os

from database_client import table
from database_models import normalize_id, update_result


def conditional_update(document_id, updates, expected_version):
    key = {"id": normalize_id(document_id)}
    expression_values = {":version": expected_version}
    update_parts = []
    for idx, (name, value) in enumerate(updates.items()):
        placeholder = f":v{idx}"
        update_parts.append(f"{name} = {placeholder}")
        expression_values[placeholder] = value
    expression_values[":next_version"] = expected_version + 1
    update_expression = "SET " + ", ".join(update_parts + ["version = :next_version"]) if update_parts else "SET version = :next_version"
    response = table().update_item(
        Key=key,
        UpdateExpression=update_expression,
        ConditionExpression="version = :version",
        ExpressionAttributeValues=expression_values,
        ReturnValues="ALL_NEW",
    )
    return update_result(response.get("Attributes", {}))


def main():
    document_id = os.environ.get("DOCUMENT_ID")
    expected_version = int(os.environ.get("EXPECTED_VERSION", "0"))
    updates = json.loads(os.environ.get("DOCUMENT_UPDATES", "{}"))
    print(json.dumps(conditional_update(document_id, updates, expected_version)))


if __name__ == "__main__":
    main()
