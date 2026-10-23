from typing import Dict, Any
from azure.cosmos import CosmosClient, PartitionKey
import os
from document_models import NormalizedExpense
from uuid import uuid4


class ExpenseRecordStore:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
        self.key = os.getenv("AZURE_COSMOS_KEY")
        self.database_name = os.getenv("AZURE_COSMOS_DATABASE", "ExpenseDB")
        self.container_name = os.getenv("AZURE_COSMOS_CONTAINER", "Expenses")
        self.client = CosmosClient(self.endpoint, self.key)
        self.database = self.client.get_database_client(self.database_name)
        self.container = self.database.get_container_client(self.container_name)

    def store_expense(self, expense: NormalizedExpense) -> Dict[str, Any]:
        expense_dict = expense.dict()
        expense_dict["id"] = expense.expense_id or str(uuid4())
        response = self.container.create_item(body=expense_dict)
        return {
            "id": response["id"],
            "status": "stored",
            "resource_id": response["_rid"],
        }

    def get_expense(self, expense_id: str) -> Dict[str, Any]:
        query = "SELECT * FROM c WHERE c.id = @expense_id"
        items = list(
            self.container.query_items(
                query=query,
                parameters=[{"name": "@expense_id", "value": expense_id}],
                enable_cross_partition_query=True,
            )
        )
        return items[0] if items else None
