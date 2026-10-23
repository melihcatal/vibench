import json
from typing import Any, Dict, List, Optional

class Document:
    """Represents a generic document in the NoSQL store."""
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def to_dict(self) -> Dict[str, Any]:
        return self._data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Document':
        return cls(data)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any):
        self._data[key] = value

class RequestHelper:
    """Helper for preparing requests to the NoSQL store."""
    @staticmethod
    def prepare_upsert_request(document_id: str, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepares a request for upserting a document."""
        return {
            "documentId": document_id,
            "data": document_data
        }

    @staticmethod
    def prepare_fetch_request(document_id: str) -> Dict[str, Any]:
        """Prepares a request for fetching a document."""
        return {
            "documentId": document_id
        }

    @staticmethod
    def prepare_query_request(field_name: str, field_value: Any) -> Dict[str, Any]:
        """Prepares a request for querying documents by a field value."""
        return {
            "query": {
                "fieldName": field_name,
                "fieldValue": field_value
            }
        }

class ResponseHelper:
    """Helper for processing responses from the NoSQL store."""
    @staticmethod
    def parse_document_response(response_data: Dict[str, Any]) -> Optional[Document]:
        """Parses a single document response."""
        if response_data and "data" in response_data:
            return Document(response_data["data"])
        return None

    @staticmethod
    def parse_query_response(response_data: Dict[str, Any]) -> List[Document]:
        """Parses a query response containing multiple documents."""
        documents = []
        if response_data and "documents" in response_data and isinstance(response_data["documents"], list):
            for doc_data in response_data["documents"]:
                documents.append(Document(doc_data))
        return documents

class DocumentNormalizer:
    """Helper for normalizing document data."""
    @staticmethod
    def normalize_document(document_data: Dict[str, Any]) -> Dict[str, Any]:
        """Applies basic normalization to document data.
        This is a placeholder for actual normalization logic (e.g.,
        type conversions, default values, cleaning).
        """
        normalized_data = {}
        for key, value in document_data.items():
            # Example: Strip whitespace from string values
            if isinstance(value, str):
                normalized_data[key] = value.strip()
            else:
                normalized_data[key] = value
        return normalized_data
