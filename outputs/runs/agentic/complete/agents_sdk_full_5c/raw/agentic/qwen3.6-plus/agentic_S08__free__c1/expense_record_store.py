"""
Persist normalized expense records in Azure Cosmos DB document store.

Stores and retrieves normalized expense records using Azure Cosmos DB's
NoSQL document database for scalable expense management.

Provider: Azure Cosmos DB
SDK: azure-cosmos
API: https://{account-name}.documents.azure.com/
"""

import json
import os
from datetime import datetime
from typing import Any, Optional

from azure.cosmos import CosmosClient, PartitionKey, exceptions


AZURE_COSMOS_ENDPOINT = os.environ.get(
    "AZURE_COSMOS_ENDPOINT",
    "https://your-account.documents.azure.com:443/",
)
AZURE_COSMOS_KEY = os.environ.get("AZURE_COSMOS_KEY", "")
AZURE_COSMOS_DATABASE = os.environ.get("AZURE_COSMOS_DATABASE", "expense-records")
AZURE_COSMOS_CONTAINER = os.environ.get("AZURE_COSMOS_CONTAINER", "expenses")


def get_cosmos_client(
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> CosmosClient:
    """
    Initialize and return an Azure Cosmos DB client.

    Args:
        endpoint: Azure Cosmos DB account endpoint URL.
                  Falls back to AZURE_COSMOS_ENDPOINT env var.
        key: Azure Cosmos DB account key.
             Falls back to AZURE_COSMOS_KEY env var.

    Returns:
        CosmosClient instance configured for document operations.

    Raises:
        ValueError: If credentials are not provided.
    """
    ep = endpoint or AZURE_COSMOS_ENDPOINT
    account_key = key or AZURE_COSMOS_KEY

    if not ep or not account_key:
        raise ValueError(
            "Azure Cosmos DB credentials are required. "
            "Set AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY environment variables."
        )

    client = CosmosClient(ep, credential=account_key)
    return client


def get_or_create_container(
    client: CosmosClient,
    database_name: str = AZURE_COSMOS_DATABASE,
    container_name: str = AZURE_COSMOS_CONTAINER,
    partition_key_path: str = "/vendor",
) -> Any:
    """
    Get or create the expense records container in Azure Cosmos DB.

    Args:
        client: CosmosClient instance.
        database_name: Database name.
        container_name: Container name.
        partition_key_path: Partition key path for the container.

    Returns:
        ContainerProxy instance for the expense records container.
    """
    database = client.create_database_if_not_exists(id=database_name)

    try:
        container = database.get_container_client(container_name)
    except exceptions.CosmosResourceNotFoundError:
        container = database.create_container(
            id=container_name,
            partition_key=PartitionKey(path=partition_key_path),
            offer_throughput=400,
        )

    return container


def store_expense_record(
    expense: dict[str, Any],
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
    database_name: str = AZURE_COSMOS_DATABASE,
    container_name: str = AZURE_COSMOS_CONTAINER,
) -> dict[str, Any]:
    """
    Store a normalized expense record in Azure Cosmos DB.

    Args:
        expense: Dictionary representing a normalized expense record.
                 Should include 'expense_id', 'vendor', 'date', 'total_amount', etc.
        endpoint: Azure Cosmos DB endpoint.
        key: Azure Cosmos DB account key.
        database_name: Database name.
        container_name: Container name.

    Returns:
        The stored expense record with Cosmos DB metadata.

    Raises:
        ValueError: If credentials are not provided.
        exceptions.CosmosHttpResponseError: If the Cosmos DB operation fails.
    """
    client = get_cosmos_client(endpoint=endpoint, key=key)
    container = get_or_create_container(
        client,
        database_name=database_name,
        container_name=container_name,
    )

    # Ensure required Cosmos DB fields
    expense_doc = dict(expense)
    expense_doc["id"] = expense_doc.get("expense_id", expense.get("id", ""))
    expense_doc["_ts"] = int(datetime.utcnow().timestamp())
    expense_doc["stored_at"] = datetime.utcnow().isoformat()
    expense_doc["document_type"] = expense_doc.get("document_type", "unknown")

    # Upsert the document
    result = container.upsert_item(body=expense_doc)

    return result


def retrieve_expense_record(
    expense_id: str,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
    database_name: str = AZURE_COSMOS_DATABASE,
    container_name: str = AZURE_COSMOS_CONTAINER,
) -> Optional[dict[str, Any]]:
    """
    Retrieve an expense record from Azure Cosmos DB by ID.

    Args:
        expense_id: The expense record ID to retrieve.
        endpoint: Azure Cosmos DB endpoint.
        key: Azure Cosmos DB account key.
        database_name: Database name.
        container_name: Container name.

    Returns:
        Expense record dictionary, or None if not found.
    """
    client = get_cosmos_client(endpoint=endpoint, key=key)
    container = get_or_create_container(
        client,
        database_name=database_name,
        container_name=container_name,
    )

    try:
        item = container.read_item(item=expense_id, partition_key=None)
        return item
    except exceptions.CosmosResourceNotFoundError:
        return None


def query_expenses_by_vendor(
    vendor: str,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
    database_name: str = AZURE_COSMOS_DATABASE,
    container_name: str = AZURE_COSMOS_CONTAINER,
) -> list[dict[str, Any]]:
    """
    Query expense records by vendor name from Azure Cosmos DB.

    Args:
        vendor: Vendor name to filter by.
        endpoint: Azure Cosmos DB endpoint.
        key: Azure Cosmos DB account key.
        database_name: Database name.
        container_name: Container name.

    Returns:
        List of expense records matching the vendor.
    """
    client = get_cosmos_client(endpoint=endpoint, key=key)
    container = get_or_create_container(
        client,
        database_name=database_name,
        container_name=container_name,
    )

    query = "SELECT * FROM c WHERE c.vendor = @vendor"
    parameters = [{"name": "@vendor", "value": vendor}]

    items = list(container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True,
    ))

    return items


def list_all_expenses(
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
    database_name: str = AZURE_COSMOS_DATABASE,
    container_name: str = AZURE_COSMOS_CONTAINER,
    max_items: int = 100,
) -> list[dict[str, Any]]:
    """
    List expense records from Azure Cosmos DB.

    Args:
        endpoint: Azure Cosmos DB endpoint.
        key: Azure Cosmos DB account key.
        database_name: Database name.
        container_name: Container name.
        max_items: Maximum number of items to return.

    Returns:
        List of expense records.
    """
    client = get_cosmos_client(endpoint=endpoint, key=key)
    container = get_or_create_container(
        client,
        database_name=database_name,
        container_name=container_name,
    )

    query = f"SELECT TOP {max_items} * FROM c ORDER BY c._ts DESC"
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True,
    ))

    return items
