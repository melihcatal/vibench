import sys

from database_client import get_container
from database_models import build_response, normalize_document


def upsert_document(document):
    container = get_container()
    item = normalize_document(document)
    return container.upsert_item(item)


def main(payload):
    try:
        result = upsert_document(payload)
        return build_response(True, result)
    except Exception as exc:
        return build_response(False, error=exc)


if __name__ == "__main__":
    raise SystemExit(0)
