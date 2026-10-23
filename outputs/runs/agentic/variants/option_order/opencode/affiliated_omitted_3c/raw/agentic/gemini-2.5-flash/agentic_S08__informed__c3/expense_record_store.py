import uuid
from typing import Dict, Any
from document_client import get_cosmos_client
from document_models import NormalizedExpense
from azure.cosmos.exceptions import CosmosResourceExistsError, CosmosHttpResponseError


COSMOS_DATABASE_NAME = "ExpenseDatabase"
COSMOS_CONTAINER_NAME = "ExpenseRecords"


def persist_expense_record(normalized_expense: NormalizedExpense) -> Dict[str, Any]:
    cosmos_client = get_cosmos_client()

    try:
        database = cosmos_client.create_database_if_not_exists(id=COSMOS_DATABASE_NAME)
    except CosmosHttpResponseError as e:
        if e.status_code == 409:  # Conflict, database already exists
            database = cosmos_client.get_database_client(COSMOS_DATABASE_NAME)
        else:
            raise

    try:
        container = database.create_container_if_not_exists(
            id=COSMOS_CONTAINER_NAME, partition_key={"path": "/document_type"}
        )
    except CosmosHttpResponseError as e:
        if e.status_code == 409:  # Conflict, container already exists
            container = database.get_container_client(COSMOS_CONTAINER_NAME)
        else:
            raise

    # Convert NormalizedExpense object to a dictionary for Cosmos DB
    expense_dict = normalized_expense.__dict__.copy()
    expense_dict["id"] = str(uuid.uuid4())  # Cosmos DB requires an 'id' field

    # Convert any datetime objects to ISO format strings if present (not strictly needed for current models but good practice)
    for key, value in expense_dict.items():
        if isinstance(value, (list, dict)):
            expense_dict[key] = json.loads(json.dumps(value, default=str))

    # Persist the item
    try:
        response = container.create_item(body=expense_dict)
        return response
    except CosmosHttpResponseError as e:
        # Handle specific errors, e.g., if item with same ID already exists
        print(f"Error persisting expense record: {e}")
        raise


import json
