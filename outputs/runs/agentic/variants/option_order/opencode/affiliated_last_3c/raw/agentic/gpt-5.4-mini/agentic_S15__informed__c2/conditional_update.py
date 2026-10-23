import json
import os

from boto3.dynamodb.conditions import Attr

from database_client import get_table
from database_models import make_response


def conditional_update(document_id, updates, expected_version):
    table = get_table()
    expr = Attr("document_id").eq(document_id) & Attr("version").eq(expected_version)
    update_expr = "SET " + ", ".join(f"#{k} = :{k}" for k in updates)
    names = {f"#{k}": k for k in updates}
    values = {f":{k}": v for k, v in updates.items()}
    values[":new_version"] = expected_version + 1
    update_expr += ", #version = :new_version"
    names["#version"] = "version"
    result = table.update_item(
        Key={"document_id": document_id},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=names,
        ExpressionAttributeValues=values,
        ConditionExpression=expr,
        ReturnValues="ALL_NEW",
    )
    return make_response(True, data=result.get("Attributes", {}))


if __name__ == "__main__":
    updates = json.loads(os.environ.get("UPDATES_JSON", "{}"))
    print(
        json.dumps(
            conditional_update(
                os.environ.get("DOCUMENT_ID", ""),
                updates,
                int(os.environ.get("EXPECTED_VERSION", "0")),
            )
        )
    )
