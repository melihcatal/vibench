# database_models.py
# [HELPER] Payload shaping, response normalization and helper dataclasses for Azure Cosmos DB usage

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional

document_type_exam = 1

@dataclass
class DocumentUpsertPayload:
    """Structure for document data to be upserted."""
    id: str
    # Include any other top-level fields expected by the container
    # Example: content: str, status: str
    **extra: Any

    def to_dict(self) -> Dict[str, Any]:
        """Convert payload to a flat dict usable by the SDK."""
        payload = {"id": self.id}
        payload.update(asdict(self))
        payload.update(self.__dict__)  # include extra keyword arguments
        return payload

@dataclass
class DocumentFetchResult:
    """Result wrapper for a fetched document."""
    document: Optional[Dict[str, Any]]

@dataclass
class QueryCriteria:
    """Criteria for querying documents (field name and value)."""
    field: str
    value: Any

@dataclass
class QueryResult:
    """Wrapper for a collection of query results."""
    results: list
