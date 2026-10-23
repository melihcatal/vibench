import os
import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests


class MongoDBAtlasDocumentStore:
    def __init__(self, app_id: Optional[str] = None, api_key: Optional[str] = None, database: Optional[str] = None, collection: Optional[str] = None):
        self.app_id = app_id or os.environ.get("MONGODB_ATLAS_APP_ID")
        self.api_key = api_key or os.environ.get("MONGODB_ATLAS_API_KEY")
        self.database = database or os.environ.get("MONGODB_ATLAS_DATABASE", "expenses")
        self.collection = collection or os.environ.get("MONGODB_ATLAS_COLLECTION", "records")
        if not self.app_id or not self.api_key:
            raise ValueError("MONGODB_ATLAS_APP_ID and MONGODB_ATLAS_API_KEY are required")

    @property
    def base_url(self) -> str:
        return f"https://services.cloud.mongodb.com/api/client/v2.0/app/{self.app_id}/endpoint/data/v1/action"

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

    def persist(self, normalized_expense_record: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "document": {
                **normalized_expense_record,
                "stored_at": datetime.now(timezone.utc).isoformat(),
            },
            "database": self.database,
            "collection": self.collection,
            "dataSource": os.environ.get("MONGODB_ATLAS_DATA_SOURCE", "Cluster0"),
        }
        response = requests.post(f"{self.base_url}/insertOne", headers=self._headers(), data=json.dumps(payload), timeout=30)
        response.raise_for_status()
        return response.json()


def save_expense_record(normalized_expense_record: Dict[str, Any], app_id: Optional[str] = None, api_key: Optional[str] = None, database: Optional[str] = None, collection: Optional[str] = None) -> Dict[str, Any]:
    store = MongoDBAtlasDocumentStore(app_id=app_id, api_key=api_key, database=database, collection=collection)
    return store.persist(normalized_expense_record)
