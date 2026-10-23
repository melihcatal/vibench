# provider: Azure Cosmos DB (JSON document store)

import os
from typing import List
from pydantic import BaseModel
from document_models import NormalizedExpense, StoreRecord
from document_client import (
    get_cosmos_db_account,
    get_cosmos_db_key,
    get_cosmos_db_database,
    get_cosmos_db_container,
)

ACCOUNT = get_cosmos_db_account()
KEY = get_cosmos_db_key()
DATABASE = get_cosmos_db_database()
CONTAINER = get_cosmos_db_container()

from azure.cosmos import CosmosClient, PartitionKey

cosmos_client = CosmosClient(ACCOUNT, credential=KEY)

database = cosmos_client.get_database_client(DATABASE)
container = database.get_container_client(CONTAINER)


class StoreRecordModel(BaseModel):
    expense_id: str
    normalized: dict
    moderation: Optional[dict]
    translation: Optional[dict]


def store_expense_record(record: StoreRecord) -> str:
    """Persist a normalized expense record (with optional moderation/translation) to Cosmos DB."""
    # Convert pydantic models to plain dicts for storage
    payload = {
        "id": record.expense_id,
        "normalized": record.normalized.dict(exclude_unset=True),
        "moderation": record.moderation.dict(exclude_unset=True)
        if record.moderation
        else None,
        "translation": record.translation.dict(exclude_unset=True)
        if record.translation
        else None,
    }
    try:
        container.upsert_item(payload)
        print(f"Stored expense {record.expense_id} successfully.")
        return record.expense_id
    except Exception as exc:
        raise RuntimeError(f"Failed to store expense {record.expense_id}: {exc}")


if __name__ == "__main__":
    # Demo insertion using a fabricated StoreRecord
    demo_record = StoreRecord(
        expense_id="EXP-2024-001",
        normalized=NormalizedExpense(
            vendor="Acme Corp",
            date="2024-07-10",
            total="$250.00",
            line_items=[{"description": "Widget", "quantity": "2", "amount": "$100"}],
            confidence="high",
        ),
        moderation=None,
        translation=None,
    )
    store_expense_record(demo_record)
