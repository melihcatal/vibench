import os
from typing import Dict, Any
from azure.cosmos import CosmosClient, PartitionKey
from document_models import NormalizedExpense


def store_expense_record(expense_data: NormalizedExpense) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")  # Concrete Azure Cosmos DB endpoint
    key = os.getenv("AZURE_COSMOS_KEY")  # Concrete Azure Cosmos DB key
    client = CosmosClient(endpoint, key)

    database_name = "ExpenseDatabase"
    container_name = "ExpenseRecords"

    database = client.create_database_if_not_exists(id=database_name)
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/expense_type")
    )

    item = expense_data.dict()
    item["id"] = f"{expense_data.expense_type}_{hash(str(item))}"

    container.create_item(body=item)

    return {"status": "success", "id": item["id"]}