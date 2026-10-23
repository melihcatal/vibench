"""
Persist normalized expense records in Azure Cosmos DB for NoSQL.

Provider: Azure Cosmos DB (azure-cosmos SDK)
Auth: AZURE_COSMOS_ENDPOINT, AZURE_COSMOS_KEY environment variables
"""

import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime

from azure.cosmos import CosmosClient, PartitionKey, exceptions


DATABASE_NAME = "expenses"
CONTAINER_NAME = "expense_records"


def get_cosmos_client() -> CosmosClient:
    """
    Initialize and return an Azure Cosmos DB client.

    Requires AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY environment variables.

    Returns:
        CosmosClient instance connected to the Azure Cosmos DB account.
    """
    endpoint = os.environ.get("AZURE_COSMOS_ENDPOINT")
    key = os.environ.get("AZURE_COSMOS_KEY")
    if not endpoint:
        raise ValueError(
            "AZURE_COSMOS_ENDPOINT environment variable is required for Azure Cosmos DB."
        )
    if not key:
        raise ValueError(
            "AZURE_COSMOS_KEY environment variable is required for Azure Cosmos DB."
        )
    return CosmosClient(endpoint, credential=key)


def ensure_database_and_container(
    client: CosmosClient,
    database_name: str = DATABASE_NAME,
    container_name: str = CONTAINER_NAME,
) -> object:
    """
    Ensure the Cosmos DB database and container exist, creating them if needed.

    Args:
        client: CosmosClient instance.
        database_name: Name of the database.
        container_name: Name of the container.

    Returns:
        Container instance for the expense records.
    """
    try:
        database = client.create_database(id=database_name)
    except exceptions.CosmosResourceExistsError:
        database = client.get_database_client(database_name)

    partition_key = PartitionKey(path="/document_type")

    try:
        container = database.create_container(
            id=container_name,
            partition_key=partition_key,
            offer_throughput=400,
        )
    except exceptions.CosmosResourceExistsError:
        container = database.get_container_client(container_name)

    return container


def store_expense_record(
    expense_dict: Dict[str, Any],
    database_name: str = DATABASE_NAME,
    container_name: str = CONTAINER_NAME,
) -> Dict[str, Any]:
    """
    Persist a normalized expense record in Azure Cosmos DB.

    Args:
        expense_dict: Dictionary representation of a NormalizedExpense record.
                      Must include 'expense_id' and 'document_type' fields.
        database_name: Cosmos DB database name.
        container_name: Cosmos DB container name.

    Returns:
        Dictionary with storage result including stored item and metadata.

    Raises:
        ValueError: If required fields are missing from the expense dict.
    """
    if "expense_id" not in expense_dict:
        raise ValueError("Expense record must contain 'expense_id' field.")
    if "document_type" not in expense_dict:
        raise ValueError("Expense record must contain 'document_type' field.")

    client = get_cosmos_client()
    container = ensure_database_and_container(
        client, database_name=database_name, container_name=container_name
    )

    item = dict(expense_dict)
    item["id"] = item["expense_id"]
    item["stored_at"] = datetime.utcnow().isoformat()
    item["provider"] = "azure_cosmos_db"

    try:
        created_item = container.upsert_item(body=item)
        return {
            "status": "stored",
            "expense_id": created_item["id"],
            "document_type": created_item["document_type"],
            "stored_at": created_item.get("stored_at"),
            "_etag": created_item.get("_etag"),
        }
    except Exception as e:
        return {
            "status": "error",
            "expense_id": item["id"],
            "error": str(e),
        }


def store_batch_expense_records(
    expenses: List[Dict[str, Any]],
    database_name: str = DATABASE_NAME,
    container_name: str = CONTAINER_NAME,
) -> List[Dict[str, Any]]:
    """
    Persist a batch of normalized expense records in Azure Cosmos DB.

    Args:
        expenses: List of expense dictionaries to store.
        database_name: Cosmos DB database name.
        container_name: Cosmos DB container name.

    Returns:
        List of storage result dictionaries, one per expense record.
    """
    client = get_cosmos_client()
    container = ensure_database_and_container(
        client, database_name=database_name, container_name=container_name
    )

    results = []
    for expense in expenses:
        try:
            item = dict(expense)
            item["id"] = item["expense_id"]
            item["stored_at"] = datetime.utcnow().isoformat()
            item["provider"] = "azure_cosmos_db"

            created_item = container.upsert_item(body=item)
            results.append({
                "status": "stored",
                "expense_id": created_item["id"],
                "document_type": created_item["document_type"],
            })
        except Exception as e:
            results.append({
                "status": "error",
                "expense_id": expense.get("expense_id", "unknown"),
                "error": str(e),
            })

    return results


def query_expense_by_id(
    expense_id: str,
    database_name: str = DATABASE_NAME,
    container_name: str = CONTAINER_NAME,
) -> Optional[Dict[str, Any]]:
    """
    Query an expense record by ID from Azure Cosmos DB.

    Args:
        expense_id: The unique expense identifier.
        database_name: Cosmos DB database name.
        container_name: Cosmos DB container name.

    Returns:
        Expense record dictionary if found, None otherwise.
    """
    client = get_cosmos_client()
    container = ensure_database_and_container(
        client, database_name=database_name, container_name=container_name
    )

    query = "SELECT * FROM c WHERE c.id = @id"
    parameters = [{"name": "@id", "value": expense_id}]

    items = list(container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True,
    ))

    return items[0] if items else None


def query_expenses_by_vendor(
    vendor_name: str,
    database_name: str = DATABASE_NAME,
    container_name: str = CONTAINER_NAME,
) -> List[Dict[str, Any]]:
    """
    Query expense records by vendor name from Azure Cosmos DB.

    Args:
        vendor_name: The vendor name to search for.
        database_name: Cosmos DB database name.
        container_name: Cosmos DB container name.

    Returns:
        List of matching expense record dictionaries.
    """
    client = get_cosmos_client()
    container = ensure_database_and_container(
        client, database_name=database_name, container_name=container_name
    )

    query = "SELECT * FROM c WHERE c.source_vendor = @vendor"
    parameters = [{"name": "@vendor", "value": vendor_name}]

    items = list(container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True,
    ))

    return items
