import os
import uuid
from azure.cosmos import CosmosClient
from document_models import NormalizedExpense


def expense_record_store(normalized_record: dict) -> str:
    endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    key = os.getenv("AZURE_COSMOS_KEY")
    client = CosmosClient(endpoint, credential=key)
    database = client.get_database_client("ExpenseDB")
    container = database.get_container_client("Expenses")

    if "id" not in normalized_record:
        normalized_record["id"] = str(uuid.uuid4())
    container.upsert_item(normalized_record)
    return normalized_record["id"]
