import os
from typing import Dict, Any
from azure.cosmos import CosmosClient, PartitionKey
from document_models import NormalizedExpense


def store_expense_record(expense: NormalizedExpense) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")
    client = CosmosClient(endpoint, key)

    database_name = "ExpenseDatabase"
    container_name = "ExpenseRecords"

    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/source_type"),
    )

    item = expense.dict()
    response = container.create_item(body=item)
    return {
        "id": response["id"],
        "status": "stored",
    }