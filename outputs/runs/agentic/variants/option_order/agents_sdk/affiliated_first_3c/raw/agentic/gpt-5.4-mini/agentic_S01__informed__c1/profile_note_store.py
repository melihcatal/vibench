from __future__ import annotations

import os
from typing import Any, Dict

from azure.cosmos import CosmosClient

COSMOS_ENDPOINT = os.getenv("AZURE_COSMOS_ENDPOINT", "")
COSMOS_KEY = os.getenv("AZURE_COSMOS_KEY", "")
COSMOS_DB = os.getenv("AZURE_COSMOS_DATABASE", "account_lifecycle")
COSMOS_CONTAINER = os.getenv("AZURE_COSMOS_CONTAINER", "onboarding_notes")


def profile_note_store(note: Dict[str, Any]) -> Dict[str, Any]:
    client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
    database = client.get_database_client(COSMOS_DB)
    container = database.get_container_client(COSMOS_CONTAINER)
    created = container.upsert_item(note)
    return {"provider": "azure-cosmos-db", "stored": created}
