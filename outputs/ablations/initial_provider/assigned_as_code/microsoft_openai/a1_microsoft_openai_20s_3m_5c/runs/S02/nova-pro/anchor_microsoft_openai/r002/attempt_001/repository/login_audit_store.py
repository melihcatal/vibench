import azure.cosmos.cosmos_client as cosmos


def store_audit_record(record, config):
    client = cosmos.CosmosClient(url=config['url'], credential=config['key'])
    database = client.get_database_client(config['database'])
    container = database.get_container_client(config['container'])
    container.create_item(record)