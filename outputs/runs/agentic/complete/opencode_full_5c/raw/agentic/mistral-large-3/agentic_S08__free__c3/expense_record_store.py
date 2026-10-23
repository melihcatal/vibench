import os
from typing import Dict, Any
from azure.cosmos import CosmosClient, PartitionKey


class ExpenseRecordStore:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_COSMOS_DB_ENDPOINT")
        self.key = os.getenv("AZURE_COSMOS_DB_KEY")
        self.database_name = os.getenv("AZURE_COSMOS_DB_DATABASE", "ExpenseDB")
        self.container_name = os.getenv("AZURE_COSMOS_DB_CONTAINER", "Expenses")
        self.client = CosmosClient(self.endpoint, credential=self.key)
        self.database = self.client.create_database_if_not_exists(id=self.database_name)
        self.container = self.database.create_container_if_not_exists(
            id=self.container_name,
            partition_key=PartitionKey(path="/document_type"),
        )

    def store_expense_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        stored_record = self.container.create_item(body=record)
        return {
            "id": stored_record["id"],
            "document_type": stored_record["document_type"],
            "total": stored_record["total"],
            "date": stored_record["date"],
        }

    def get_expense_record(self, record_id: str) -> Dict[str, Any]:
        return self.container.read_item(item=record_id, partition_key=record_id)
