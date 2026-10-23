import json
from typing import Any, Dict

from azure.cosmos import exceptions

from database_client import create_client, get_container


def fetch_document(document_id: str) -> Dict[str, Any]:
    client = create_client()
    container = get_container(client)
    return container.read_item(item=document_id, partition_key=document_id)


def main() -> None:
    import sys
    print(json.dumps(fetch_document(sys.argv[1])))


if __name__ == "__main__":
    main()
