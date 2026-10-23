import json
import sys

from database_client import get_table
from database_models import build_error_response, build_success_response


def fetch_document(identifier_name, identifier_value):
    table = get_table()
    result = table.get_item(
        Key={identifier_name: identifier_value}, ConsistentRead=True
    )
    return build_success_response(item=result.get("Item"), message="fetched")


def main():
    try:
        payload = json.loads(sys.stdin.read())
        print(
            json.dumps(
                fetch_document(payload["identifier_name"], payload["identifier_value"])
            )
        )
    except Exception as exc:
        print(json.dumps(build_error_response(exc)))


if __name__ == "__main__":
    main()
