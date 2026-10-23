import datetime
from typing import Any, Dict, List, Optional


class DocumentRequest:
    def __init__(
        self,
        document_id: str,
        data: Optional[Dict[str, Any]] = None,
        partition_key: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ):
        self.document_id = document_id
        self.data = data or {}
        self.partition_key = partition_key
        self.fields = fields

    def to_mongo_filter(self) -> Dict[str, Any]:
        if self.partition_key:
            return {"_id": self.document_id, "partition_key": self.partition_key}
        return {"_id": self.document_id}

    def to_upsert_payload(self) -> Dict[str, Any]:
        payload = dict(self.data)
        payload["_id"] = self.document_id
        if self.partition_key:
            payload["partition_key"] = self.partition_key
        payload["updated_at"] = datetime.datetime.utcnow()
        if "created_at" not in payload:
            payload["created_at"] = payload["updated_at"]
        return payload


class DocumentResponse:
    def __init__(
        self,
        success: bool,
        document: Optional[Dict[str, Any]] = None,
        documents: Optional[List[Dict[str, Any]]] = None,
        matched_count: int = 0,
        modified_count: int = 0,
        upserted_id: Optional[str] = None,
        error: Optional[str] = None,
    ):
        self.success = success
        self.document = document
        self.documents = documents or []
        self.matched_count = matched_count
        self.modified_count = modified_count
        self.upserted_id = upserted_id
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "success": self.success,
            "matched_count": self.matched_count,
            "modified_count": self.modified_count,
        }
        if self.document is not None:
            result["document"] = _serialize_document(self.document)
        if self.documents:
            result["documents"] = [_serialize_document(d) for d in self.documents]
        if self.upserted_id is not None:
            result["upserted_id"] = self.upserted_id
        if self.error:
            result["error"] = self.error
        return result


class ConditionalUpdateRequest:
    def __init__(
        self,
        document_id: str,
        update_fields: Dict[str, Any],
        condition: Optional[Dict[str, Any]] = None,
        version: Optional[int] = None,
        partition_key: Optional[str] = None,
    ):
        self.document_id = document_id
        self.update_fields = update_fields
        self.condition = condition
        self.version = version
        self.partition_key = partition_key

    def to_mongo_filter(self) -> Dict[str, Any]:
        query = {"_id": self.document_id}
        if self.partition_key:
            query["partition_key"] = self.partition_key
        if self.version is not None:
            query["version"] = self.version
        if self.condition:
            query.update(self.condition)
        return query

    def to_mongo_update(self) -> Dict[str, Any]:
        update = {"$set": dict(self.update_fields)}
        update["$set"]["updated_at"] = datetime.datetime.utcnow()
        if self.version is not None:
            update["$inc"] = {"version": 1}
        return update


class QueryRequest:
    def __init__(
        self,
        field: str,
        value: Any,
        partition_key: Optional[str] = None,
        limit: int = 100,
        sort_field: Optional[str] = None,
        sort_order: int = 1,
        projection: Optional[List[str]] = None,
    ):
        self.field = field
        self.value = value
        self.partition_key = partition_key
        self.limit = limit
        self.sort_field = sort_field
        self.sort_order = sort_order
        self.projection = projection

    def to_mongo_filter(self) -> Dict[str, Any]:
        query = {self.field: self.value}
        if self.partition_key:
            query["partition_key"] = self.partition_key
        return query

    def to_mongo_projection(self) -> Optional[Dict[str, int]]:
        if self.projection:
            return {f: 1 for f in self.projection}
        return None


def _serialize_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    result = {}
    for key, value in doc.items():
        if isinstance(value, datetime.datetime):
            result[key] = value.isoformat()
        elif isinstance(value, dict):
            result[key] = _serialize_document(value)
        else:
            result[key] = value
    return result


def normalize_mongo_id(doc: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(doc)
    if "_id" in result:
        result["id"] = str(result["_id"])
        del result["_id"]
    return result
