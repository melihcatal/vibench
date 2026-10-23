import json

from messaging_client import dynamodb_resource


def store_audit_record(table_name: str, record: dict) -> dict:
    table = dynamodb_resource().Table(table_name)
    table.put_item(Item=record)
    return {"stored": True, "record_id": record.get("record_id", "")}


def main() -> None:
    import sys

    data = json.loads(sys.stdin.read() or "{}")
    print(json.dumps(store_audit_record(data["table_name"], data.get("record", {}))))


if __name__ == "__main__":
    main()
