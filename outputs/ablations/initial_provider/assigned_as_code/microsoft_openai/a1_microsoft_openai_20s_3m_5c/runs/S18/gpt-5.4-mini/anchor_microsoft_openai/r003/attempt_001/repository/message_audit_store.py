from azure.data.tables import TableServiceClient


def store_message_audit(record, config=None):
    config = config or {}
    service = TableServiceClient.from_connection_string(config['connection_string'])
    table = service.get_table_client(table_name=config['table'])
    entity = dict(record)
    entity['PartitionKey'] = entity.get('PartitionKey', 'messages')
    entity['RowKey'] = entity.get('RowKey', entity.get('message_id', 'unknown'))
    table.upsert_entity(entity)
    return {'stored': True, 'row_key': entity['RowKey']}
