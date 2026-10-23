from typing import Dict, Any
import os
from azure.cosmos import CosmosClient, PartitionKey
from document_models import NormalizedExpense


class ExpenseRecordStore:
    def __init__(self):
        self.endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
        self.key = os.getenv("AZURE_COSMOS_KEY")
        self.database_name = os.getenv("AZURE_COSMOS_DATABASE", "ExpenseDatabase")
        self.container_name = os.getenv("AZURE_COSMOS_CONTAINER", "ExpenseRecords")
        self.client = CosmosClient(self.endpoint, credential=self.key)
        self.database = self.client.create_database_if_not_exists(id=self.database_name)
        self.container = self.database.create_container_if_not_exists(
            id=self.container_name, partition_key=PartitionKey(path="/vendor_merchant")
        )

    def store_expense(self, expense_data: Dict[str, Any]) -> Dict[str, Any]:
        expense = NormalizedExpense(**expense_data)
        item = expense.dict()
        item["id"] = (
            f"expense_{item.get('vendor_merchant', 'unknown')}_{item.get('date', 'undated')}"
        )

        response = self.container.create_item(body=item)
        return {
            "id": response["id"],
            "status": "stored",
            "request_charge": response["requestCharge"],
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
        return items[0] if items else {}

    def update_expense(
        self, expense_id: str, updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        query = "SELECT * FROM c WHERE c.id = @expense_id"
        items = list(
            self.container.query_items(
                query=query,
                parameters=[{"name": "@expense_id", "value": expense_id}],
                enable_cross_partition_query=True,
            )
        )

        if not items:
            return {"status": "not_found"}

        item = items[0]
        item.update(updates)
        response = self.container.replace_item(item["id"], item)
        return {
            "id": response["id"],
            "status": "updated",
            "request_charge": response["requestCharge"],
        }
