from azure.cosmos import CosmosClient

from database_client import load_config


def conditional_update(payload, config=None):
    cfg = load_config(config)
    with CosmosClient(cfg['endpoint'], credential=cfg['api_key']) as client:
        container = client.get_database_client(cfg['database']).get_container_client(cfg['container'])
        existing = container.read_item(item=payload['id'], partition_key=payload.get('partition_key', payload['id']))
        expected = payload.get('etag') or payload.get('version')
        if expected is not None and existing.get('_etag') not in (expected, str(expected)) and existing.get('version') != expected:
            return {'updated': False, 'document': existing}
        updated = dict(existing)
        updated.update(payload.get('updates', {}))
        container.upsert_item(updated)
    return {'updated': True, 'document': updated}
