import os
from azure.cosmos import CosmosClient, PartitionKey
from typing import Dict, Any


def persist_expense_record(record: Dict[str, Any], config=None):
    config = config or {}
    cosmos_endpoint = config.get('AZURE_COSMOS_ENDPOINT', os.environ.get('AZURE_COSMOS_ENDPOINT'))
    cosmos_key = config.get('AZURE_COSMOS_KEY', os.environ.get('AZURE_COSMOS_KEY'))
    database_name = config.get('AZURE_COSMOS_DATABASE_NAME', os.environ.get('AZURE_COSMOS_DATABASE_NAME', 'ExpenseRecordsDB'))
    container_name = config.get('AZURE_COSMOS_CONTAINER_NAME', os.environ.get('AZURE_COSMOS_CONTAINER_NAME', 'Expenses'))

    if not cosmos_endpoint or not cosmos_key:
        raise ValueError("Azure Cosmos DB endpoint and key must be provided in config or environment variables.")

    client = CosmosClient(cosmos_endpoint, cosmos_key)
    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/document_type"),
        offer_throughput=400
    )

    try:
        # Cosmos DB requires an 'id' field for items
        if 'id' not in record:
            import uuid
            record['id'] = str(uuid.uuid4())
        container.upsert_item(body=record)
        return {'status': 'success', 'id': record['id']}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
