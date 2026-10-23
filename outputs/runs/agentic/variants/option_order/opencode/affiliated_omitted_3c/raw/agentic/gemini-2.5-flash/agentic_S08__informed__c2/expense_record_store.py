from document_client import get_cosmos_client
from document_models import NormalizedExpense
from azure.cosmos.exceptions import CosmosResourceExistsError, CosmosHttpResponseError


def persist_expense_record(
    expense: NormalizedExpense, database_name: str, container_name: str
):
    client = get_cosmos_client()

    try:
        database = client.create_database_if_not_exists(id=database_name)
        container = database.create_container_if_not_exists(
            id=container_name,
            partition_key={"paths": ["/transaction_type"], "kind": "Hash"},
        )
    except CosmosResourceExistsError:
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)
    except CosmosHttpResponseError as e:
        print(f"Error creating database or container: {e}")
        raise

    # Convert dataclass to dict for Cosmos DB
    expense_dict = expense.__dict__
    # Cosmos DB requires an 'id' field
    expense_dict["id"] = expense.document_id

    try:
        container.upsert_item(body=expense_dict)
        return {"status": "success", "document_id": expense.document_id}
    except CosmosHttpResponseError as e:
        print(f"Error persisting expense record: {e}")
        raise
