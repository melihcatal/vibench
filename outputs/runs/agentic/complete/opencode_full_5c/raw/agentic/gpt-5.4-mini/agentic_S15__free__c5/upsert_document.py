import json
import sys
from typing import Any, Dict

from database_client import get_table
from database_models import normalize_document


def upsert_document(document_id: str, document: Dict[str, Any]) -> Dict[str, Any]:
    table = get_table()
    item = normalize_document(document)
    item["document_id"] = document_id
    table.put_item(Item=item)
    return item


def main() -> None:
    payload = json.loads(sys.stdin.read())
    document_id = str(payload["document_id"])
    document = dict(payload["document"])
    result = upsert_document(document_id, document)
    sys.stdout.write(json.dumps(result, default=str))


if __name__ == "__main__":
    main()
