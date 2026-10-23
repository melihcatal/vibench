import json
from typing import Any, Dict

from azure.cosmos import exceptions

from database_client import create_client, get_container
from database_models import normalize_document


def upsert_document(document: Dict[str, Any]) -> Dict[str, Any]:
    client = create_client()
    container = get_container(client)
    payload = normalize_document(document)
    result = container.upsert_item(payload)
    return dict(result)


def main() -> None:
    import sys
    document = json.loads(sys.stdin.read())
    print(json.dumps(upsert_document(document)))


if __name__ == "__main__":
    main()
