from azure.data.tables import TableServiceClient
from messaging_models import build_message_record
from messaging_client import load_messaging_config


def store_message_audit(record, config=None):
    cfg = load_messaging_config(config)
    service = TableServiceClient.from_connection_string(cfg['connection_string'])
    table = service.get_table_client(cfg['audit_table'])
    entity = build_message_record(message_id=record.get('message_id'), payload=record.get('payload'), status=record.get('status'), details=record.get('details'))
    entity.update({'PartitionKey': 'messages', 'RowKey': entity['message_id'] or 'unknown'})
    table.upsert_entity(entity)
    return entity
