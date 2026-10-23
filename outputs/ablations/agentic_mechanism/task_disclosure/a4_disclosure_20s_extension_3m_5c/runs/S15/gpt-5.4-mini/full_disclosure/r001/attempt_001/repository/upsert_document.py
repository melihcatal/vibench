import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class CosmosConfig:
    endpoint: str = os.environ.get("AZURE_COSMOS_ENDPOINT", "")
    key: str = os.environ.get("AZURE_COSMOS_KEY", "")
    database: str = os.environ.get("AZURE_COSMOS_DATABASE", "")
    container: str = os.environ.get("AZURE_COSMOS_CONTAINER", "")
    api_version: str = os.environ.get("AZURE_COSMOS_API_VERSION", "2018-12-31")


class CosmosDBClient:
    def __init__(self, config: Optional[CosmosConfig] = None) -> None:
        self.config = config or CosmosConfig()
        if not self.config.endpoint or not self.config.key or not self.config.database or not self.config.container:
            raise ValueError("Missing Azure Cosmos DB configuration")
        self._session = requests.Session()

    def upsert_document(self, document: Dict[str, Any], partition_key: Optional[Any] = None) -> Dict[str, Any]:
        if not isinstance(document, dict):
            raise TypeError("document must be a JSON object")
        document_id = document.get("id")
        if not document_id:
            raise ValueError("document must include an 'id' field")
        payload = json.dumps(document, separators=(",", ":"), ensure_ascii=False)
        url = f"{self.config.endpoint.rstrip('/')}/dbs/{self.config.database}/colls/{self.config.container}/docs"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-ms-date": "Thu, 01 Jan 1970 00:00:00 GMT",
            "x-ms-version": self.config.api_version,
            "x-ms-documentdb-is-upsert": "True",
            "Authorization": self.config.key,
        }
        if partition_key is not None:
            headers["x-ms-documentdb-partitionkey"] = json.dumps([partition_key])
        response = self._session.post(url, data=payload, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()


def upsert_document(document: Dict[str, Any], partition_key: Optional[Any] = None) -> Dict[str, Any]:
    return CosmosDBClient().upsert_document(document, partition_key=partition_key)


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: upsert_document.py '{\"id\": \"1\", ...}'")
    document = json.loads(sys.argv[1])
    result = upsert_document(document)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
