from database_client import get_container
from database_models import build_response, normalize_identifier


def fetch_document(identifier):
    container = get_container()
    return container.read_item(item=normalize_identifier(identifier)["id"], partition_key=normalize_identifier(identifier)["id"])


def main(identifier):
    try:
        result = fetch_document(identifier)
        return build_response(True, result)
    except Exception as exc:
        return build_response(False, error=exc)
