import json
import sys

from boto3.dynamodb.conditions import Attr

from database_client import get_table
from database_models import build_error_response, build_success_response


def conditional_update(
    identifier_name,
    identifier_value,
    update_expression,
    expression_attribute_values,
    condition_expression=None,
):
    table = get_table()
    kwargs = {
        "Key": {identifier_name: identifier_value},
        "UpdateExpression": update_expression,
        "ExpressionAttributeValues": expression_attribute_values,
        "ReturnValues": "ALL_NEW",
    }
    if condition_expression is not None:
        kwargs["ConditionExpression"] = condition_expression
    result = table.update_item(**kwargs)
    return build_success_response(item=result.get("Attributes"), message="updated")


def main():
    try:
        payload = json.loads(sys.stdin.read())
        print(
            json.dumps(
                conditional_update(
                    payload["identifier_name"],
                    payload["identifier_value"],
                    payload["update_expression"],
                    payload["expression_attribute_values"],
                    payload.get("condition_expression"),
                )
            )
        )
    except Exception as exc:
        print(json.dumps(build_error_response(exc)))


if __name__ == "__main__":
    main()
