from database_client import get_container
from database_models import normalize_document


def fetch_document(payload, config=None):
    container = get_container(config)
    document = container.read_item(item=payload['id'], partition_key=payload.get('partition_key', payload['id']))
    return {'document': normalize_document(document)}
