from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


@dataclass
class QueryDocumentsRequest:
    collection_id: str
    field_name: str
    field_value: Any
    limit: int = 100
    partition_key: Optional[str] = None


@dataclass
class QueryDocumentsResponse:
    documents: List[Dict[str, Any]]
    continuation_token: Optional[str] = None


class MongoDBAtlasDocumentClient:
    def __init__(self, app_id: Optional[str] = None, api_key: Optional[str] = None) -> None:
        self.app_id = app_id or os.getenv("MONGODB_ATLAS_APP_ID")
        self.api_key = api_key or os.getenv("MONGODB_ATLAS_API_KEY")
        if not self.app_id or not self.api_key:
            raise ValueError("MONGODB_ATLAS_APP_ID and MONGODB_ATLAS_API_KEY are required")
        self.base_url = f"https://realm.mongodb.com/api/client/v2.0/app/{self.app_id}/endpoint/data/v1/action"

    def query_documents(self, request: QueryDocumentsRequest) -> QueryDocumentsResponse:
        filter_doc: Dict[str, Any] = {request.field_name: request.field_value}
        if request.partition_key is not None:
            filter_doc["partition_key"] = request.partition_key
        payload: Dict[str, Any] = {
            "collection": request.collection_id,
            "database": os.getenv("MONGODB_ATLAS_DATABASE", "default"),
            "dataSource": os.getenv("MONGODB_ATLAS_DATASOURCE", "Cluster0"),
            "filter": filter_doc,
            "limit": request.limit,
        }
        response = requests.post(
            f"{self.base_url}/find",
            headers={
                "Content-Type": "application/json",
                "api-key": self.api_key,
            },
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        body = response.json()
        return QueryDocumentsResponse(
            documents=body.get("documents", []),
            continuation_token=body.get("nextBatchToken"),
        )


def query_documents(
    collection_id: str,
    field_name: str,
    field_value: Any,
    limit: int = 100,
    partition_key: Optional[str] = None,
) -> QueryDocumentsResponse:
    client = MongoDBAtlasDocumentClient()
    request = QueryDocumentsRequest(
        collection_id=collection_id,
        field_name=field_name,
        field_value=field_value,
        limit=limit,
        partition_key=partition_key,
    )
    return client.query_documents(request)
