import os
from typing import Dict, Any
from azure.cosmos import CosmosClient, PartitionKey
from document_models import NormalizedExpense


client = CosmosClient(
    os.getenv("AZURE_COSMOS_ENDPOINT"),
    credential=os.getenv("AZURE_COSMOS_KEY")
)

database_name = os.getenv("AZURE_COSMOS_DATABASE")
container_name = os.getenv("AZURE_COSMOS_CONTAINER")

database = client.get_database_client(database_name)
container = database.get_container_client(container_name)


def store_expense_record(expense: NormalizedExpense) -> Dict[str, Any]:
    document = expense.dict()
    document["id"] = f"expense_{hash(frozenset(document.items()))}"
    container.upsert_item(document)
    return {"id": document["id"], "status": "stored"}