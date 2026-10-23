from azure.cosmos import MatchConditions

from database_client import get_container_client, load_config, normalize_document
from database_models import build_update_patch


def conditional_update(payload, config=None):
    config = load_config(config)
    container = get_container_client(config)
    patch = build_update_patch(payload)
    options = {}
    if payload.get('etag'):
        options['etag'] = payload['etag']
        options['match_condition'] = MatchConditions.IfNotModified
    updated = container.patch_item(item=payload['id'], partition_key=payload.get('partition_key', payload['id']), patch_operations=patch, **options)
    return normalize_document(updated)
