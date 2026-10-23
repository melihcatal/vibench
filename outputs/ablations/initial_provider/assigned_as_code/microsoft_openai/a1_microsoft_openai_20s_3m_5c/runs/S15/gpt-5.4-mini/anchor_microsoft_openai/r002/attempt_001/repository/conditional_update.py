from database_client import get_container
from database_models import build_condition, normalize_document


def conditional_update(payload, config=None):
    container = get_container(config)
    condition = build_condition(payload.get('version'), payload.get('etag'))
    document = container.read_item(item=payload['id'], partition_key=payload.get('partition_key', payload['id']))
    current = normalize_document(document)
    if condition.get('version') is not None and current.get('version') != condition['version']:
        return {'updated': False, 'document': current}
    if condition.get('etag') is not None and current.get('_etag') != condition['etag']:
        return {'updated': False, 'document': current}
    updated = dict(current, **payload['updates'])
    container.replace_item(item=current, body=updated)
    return {'updated': True, 'document': updated}
