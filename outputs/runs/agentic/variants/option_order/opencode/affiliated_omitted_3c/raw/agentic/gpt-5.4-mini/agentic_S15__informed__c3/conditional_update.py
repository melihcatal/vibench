import json
import os

from boto3.dynamodb.conditions import Attr

from database_client import get_primary_key_name, get_table, get_version_key_name
from database_models import normalize_document, response_payload


def conditional_update(document, table_name=None):
    item = normalize_document(document)
    key_name = get_primary_key_name()
    version_key = get_version_key_name()
    if key_name not in item:
        raise ValueError(f"Missing primary identifier: {key_name}")
    if version_key not in item:
        raise ValueError(f"Missing version field: {version_key}")
    table = get_table(table_name)
    current_version = item[version_key]
    updates = dict(item)
    updates[version_key] = current_version + 1
    condition = Attr(version_key).eq(current_version)
    table.update_item(
        Key={key_name: item[key_name]},
        UpdateExpression="SET " + ", ".join(f"#{k} = :{k}" for k in updates.keys()),
        ExpressionAttributeNames={f"#{k}": k for k in updates.keys()},
        ExpressionAttributeValues={f":{k}": v for k, v in updates.items()},
        ConditionExpression=condition,
    )
    return response_payload(ok=True, document=updates)


if __name__ == "__main__":
    print(json.dumps(conditional_update(os.environ.get("DOCUMENT_JSON", "{}"))))
