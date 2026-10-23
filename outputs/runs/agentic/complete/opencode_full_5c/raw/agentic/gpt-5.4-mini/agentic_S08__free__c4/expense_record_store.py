from document_client import cosmos_client, load_config


def expense_record_store(record):
    client = cosmos_client()
    config = load_config()
    database = client.get_database_client(config.cosmos_database)
    container = database.get_container_client(config.cosmos_container)
    return container.upsert_item(record)
