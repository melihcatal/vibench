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

    def fetch_document(self, document_id: str, partition_key: Optional[Any] = None) -> Dict[str, Any]:
        if not document_id:
            raise ValueError("document_id must be provided")
        url = f"{self.config.endpoint.rstrip('/')}/dbs/{self.config.database}/colls/{self.config.container}/docs/{document_id}"
        headers = {
            "Accept": "application/json",
            "x-ms-date": "Thu, 01 Jan 1970 00:00:00 GMT",
            "x-ms-version": self.config.api_version,
            "Authorization": self.config.key,
        }
        if partition_key is not None:
            headers["x-ms-documentdb-partitionkey"] = json.dumps([partition_key])
        response = self._session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()


def fetch_document(document_id: str, partition_key: Optional[Any] = None) -> Dict[str, Any]:
    return CosmosDBClient().fetch_document(document_id, partition_key=partition_key)


def main() -> None:
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: fetch_document.py <document_id>")
    result = fetch_document(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
