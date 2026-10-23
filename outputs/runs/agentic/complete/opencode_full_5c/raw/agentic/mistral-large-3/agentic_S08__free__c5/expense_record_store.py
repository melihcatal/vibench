from typing import Dict, Any, Optional
import os
from azure.cosmos import CosmosClient, PartitionKey
from datetime import datetime


class ExpenseRecordStore:
    """
    Persists normalized expense records in Azure Cosmos DB.
    """

    def __init__(self):
        self.endpoint = os.getenv("AZURE_COSMOS_DB_ENDPOINT")
        self.key = os.getenv("AZURE_COSMOS_DB_KEY")
        self.database_name = os.getenv("AZURE_COSMOS_DB_DATABASE", "ExpenseDB")
        self.container_name = os.getenv("AZURE_COSMOS_DB_CONTAINER", "Expenses")

        if not all([self.endpoint, self.key]):
            raise ValueError("Missing Azure Cosmos DB environment variables.")

        self.client = CosmosClient(self.endpoint, credential=self.key)
        self.database = self.client.create_database_if_not_exists(id=self.database_name)
        self.container = self.database.create_container_if_not_exists(
            id=self.container_name, partition_key=PartitionKey(path="/vendor")
        )

    def store_expense(self, expense_data: Dict[str, Any]) -> str:
        """
        Stores a normalized expense record in Azure Cosmos DB.
        """
        expense_data["id"] = str(
            expense_data.get("id", f"expense_{datetime.utcnow().isoformat()}")
        )
        expense_data["created_at"] = datetime.utcnow().isoformat()

        response = self.container.create_item(body=expense_data)
        return response["id"]

    def get_expense(self, expense_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves an expense record by ID from Azure Cosmos DB.
        """
        try:
            response = self.container.read_item(
                item=expense_id, partition_key=expense_id
            )
            return response
        except Exception:
            return None
