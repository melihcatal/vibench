import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosHttpResponseError


class ExpenseRecordStore:
    """Persist normalized expense records in Azure Cosmos DB."""

    def __init__(
        self, database_name: str = "expense_db", container_name: str = "expenses"
    ):
        # Get Azure Cosmos DB credentials
        endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
        key = os.getenv("AZURE_COSMOS_KEY")

        if not endpoint or not key:
            raise ValueError(
                "AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY environment variables are required"
            )

        # Create Cosmos DB client
        self.client = CosmosClient(endpoint, key)
        self.database_name = database_name
        self.container_name = container_name

        # Initialize database and container
        self.database = self.client.create_database_if_not_exists(id=database_name)
        self.container = self.database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path="/vendor"),
            offer_throughput=400,
        )

    def store_expense_record(self, expense_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Store a normalized expense record in Cosmos DB.

        Args:
            expense_record: Normalized expense record

        Returns:
            Stored record with Cosmos DB metadata
        """
        # Prepare document for Cosmos DB
        document = {
            "id": f"expense_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}",
            "vendor": expense_record.get("vendor", {}).get("value", "unknown")
            if isinstance(expense_record.get("vendor"), dict)
            else expense_record.get("vendor", "unknown"),
            "timestamp": datetime.utcnow().isoformat(),
            "data": expense_record,
            "provider": "Azure Cosmos DB",
            "database": self.database_name,
            "container": self.container_name,
        }

        try:
            # Create item in Cosmos DB
            created_item = self.container.create_item(body=document)

            # Return stored record with Cosmos DB metadata
            stored_record = {
                "id": created_item["id"],
                "vendor": created_item["vendor"],
                "timestamp": created_item["timestamp"],
                "cosmos_metadata": {
                    "_rid": created_item.get("_rid"),
                    "_self": created_item.get("_self"),
                    "_etag": created_item.get("_etag"),
                    "_attachments": created_item.get("_attachments"),
                    "_ts": created_item.get("_ts"),
                },
                "data": created_item["data"],
                "storage_provider": "Azure Cosmos DB for NoSQL",
                "endpoint_used": os.getenv("AZURE_COSMOS_ENDPOINT"),
            }

            return stored_record

        except CosmosHttpResponseError as e:
            raise Exception(f"Cosmos DB error: {e.message}")

    def get_expense_record(self, record_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an expense record by ID.

        Args:
            record_id: Record ID to retrieve

        Returns:
            Expense record or None if not found
        """
        try:
            item = self.container.read_item(item=record_id, partition_key=record_id)
            return item
        except CosmosHttpResponseError:
            return None

    def query_expenses_by_vendor(self, vendor_name: str) -> List[Dict[str, Any]]:
        """
        Query expenses by vendor name.

        Args:
            vendor_name: Vendor name to query

        Returns:
            List of expense records
        """
        query = f"SELECT * FROM c WHERE c.vendor = @vendor"
        parameters = [{"name": "@vendor", "value": vendor_name}]

        items = list(
            self.container.query_items(
                query=query, parameters=parameters, enable_cross_partition_query=True
            )
        )

        return items

    def get_all_expenses(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all expense records (with limit).

        Args:
            limit: Maximum number of records to return

        Returns:
            List of expense records
        """
        query = f"SELECT TOP {limit} * FROM c ORDER BY c.timestamp DESC"

        items = list(
            self.container.query_items(query=query, enable_cross_partition_query=True)
        )

        return items

    def delete_expense_record(self, record_id: str) -> bool:
        """
        Delete an expense record.

        Args:
            record_id: Record ID to delete

        Returns:
            True if deleted, False if not found
        """
        try:
            self.container.delete_item(item=record_id, partition_key=record_id)
            return True
        except CosmosHttpResponseError:
            return False
