import json
import sys

from database_client import get_table


def fetch_document(document_id: str):
    table = get_table()
    response = table.get_item(Key={"document_id": document_id})
    return response.get("Item")


def main() -> None:
    payload = json.loads(sys.stdin.read())
    result = fetch_document(str(payload["document_id"]))
    sys.stdout.write(json.dumps(result, default=str))


if __name__ == "__main__":
    main()
