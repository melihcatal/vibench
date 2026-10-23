import json
from typing import Any, Dict

from azure.cosmos import exceptions

from database_client import create_client, get_container


def conditional_update(document_id: str, changes: Dict[str, Any], expected_version: int | None = None) -> Dict[str, Any]:
    client = create_client()
    container = get_container(client)
    current = container.read_item(item=document_id, partition_key=document_id)
    if expected_version is not None and current.get("version") != expected_version:
        raise ValueError("version mismatch")
    current.update(changes)
    current["version"] = int(current.get("version", 0)) + 1
    return dict(container.upsert_item(current))


def main() -> None:
    import sys
    payload = json.loads(sys.stdin.read())
    print(json.dumps(conditional_update(payload["document_id"], payload["changes"], payload.get("expected_version"))))


if __name__ == "__main__":
    main()
