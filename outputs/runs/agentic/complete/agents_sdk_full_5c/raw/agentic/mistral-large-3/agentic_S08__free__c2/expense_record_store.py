import os
from typing import Dict, Any
from azure.cosmos import CosmosClient, PartitionKey
from document_models import NormalizedExpense


def store_expense_record(expense_data: NormalizedExpense) -> str:
    """Persist normalized expense records in Azure Cosmos DB."""
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT", "https://<your-account>.documents.azure.com:443/")
    key = os.getenv("AZURE_COSMOS_KEY", "<your-key>")
    client = CosmosClient(endpoint, key)
    database_name = "ExpensesDB"
    container_name = "NormalizedExpenses"

    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/expense_type")
    )

    record = expense_data.dict()
    response = container.create_item(body=record)
    return response['id']