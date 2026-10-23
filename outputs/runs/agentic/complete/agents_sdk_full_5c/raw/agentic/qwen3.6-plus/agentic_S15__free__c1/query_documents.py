"""
query_documents.py - Queries documents by a field value or partition-style key
from MongoDB Atlas managed NoSQL document store.

Provider: MongoDB Atlas (pymongo driver for mongodb+srv:// clusters)
"""

from typing import Any, List, Optional

from database_client import AtlasClient
from database_models import DocumentRecord, QueryRequest, QueryResponse


def query_documents(request: QueryRequest) -> QueryResponse:
    """
    Query MongoDB Atlas for documents matching a field value,
    optionally scoped to a partition key.
    """
    try:
        with AtlasClient() as client:
            raw_docs = client.query_by_field(
                field_name=request.field_name,
                field_value=request.field_value,
                partition_key=request.partition_key,
                limit=request.limit,
            )

        records: List[DocumentRecord] = []
        for raw in raw_docs:
            records.append(DocumentRecord.from_mongo(raw))

        return QueryResponse(documents=records, count=len(records))

    except RuntimeError as exc:
        return QueryResponse(documents=[], count=0, error=str(exc))


def query_documents_by_field(
    field_name: str,
    field_value: Any,
    partition_key: Optional[str] = None,
    limit: int = 50,
) -> List[DocumentRecord]:
    """
    Convenience function to query documents and return a plain list.
    Raises on provider-side errors.
    """
    request = QueryRequest(
        field_name=field_name,
        field_value=field_value,
        partition_key=partition_key,
        limit=limit,
    )
    response = query_documents(request)
    if response.error:
        raise RuntimeError(response.error)
    return response.documents
