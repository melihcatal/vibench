import os
from typing import Dict, Any
from azure.cosmos import CosmosClient, PartitionKey
from document_models import ExpenseRecord


def get_expense_container():
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")
    client = CosmosClient(endpoint, key)
    database = client.get_database_client("ExpenseDatabase")
    container = database.get_container_client("ExpenseRecords")
    return container


def store_expense_record(record: ExpenseRecord) -> Dict[str, Any]:
    container = get_expense_container()
    result = container.create_item(body=record.dict())
    return {
        "id": result["id"],
        "status": "stored",
        "resource_id": result["_rid"]
    }