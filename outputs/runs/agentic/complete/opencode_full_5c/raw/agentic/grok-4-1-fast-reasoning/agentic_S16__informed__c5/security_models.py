from typing import TypedDict, Dict, Any, List, Optional


class FetchedSecret(TypedDict):
    value: Any
    metadata: Dict[str, Any]


class SecretRotation(TypedDict):
    secret_name: str
    version: str
    status: str
    notes: Optional[str]
    labels: Optional[Dict[str, str]]


class AuditNotes(TypedDict):
    notes: str
    labels: Dict[str, str]
