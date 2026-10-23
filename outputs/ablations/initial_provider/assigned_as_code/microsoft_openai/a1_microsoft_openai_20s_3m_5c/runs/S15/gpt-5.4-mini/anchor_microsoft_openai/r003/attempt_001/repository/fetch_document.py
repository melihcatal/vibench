from database_client import get_container_client, load_config, normalize_document


def fetch_document(payload, config=None):
    config = load_config(config)
    container = get_container_client(config)
    document = container.read_item(item=payload['id'], partition_key=payload.get('partition_key', payload['id']))
    return normalize_document(document)
