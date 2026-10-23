import json
import sys

from database_client import get_table
from database_models import (
    build_error_response,
    build_success_response,
    parse_json_document,
)


def upsert_document(document):
    table = get_table()
    item = parse_json_document(document)
    result = table.put_item(Item=item, ReturnConsumedCapacity="TOTAL")
    return build_success_response(
        item=item, consumed_capacity=result.get("ConsumedCapacity"), message="upserted"
    )


def main():
    try:
        document = json.loads(sys.stdin.read())
        print(json.dumps(upsert_document(document)))
    except Exception as exc:
        print(json.dumps(build_error_response(exc)))


if __name__ == "__main__":
    main()
