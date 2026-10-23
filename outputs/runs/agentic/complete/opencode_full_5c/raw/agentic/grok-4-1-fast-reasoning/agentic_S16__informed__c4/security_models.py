from typing import TypedDict, Dict, Any, List, Optional


class SecretMetadata(TypedDict):
    name: str
    version_id: Optional[str]
    created_time: Optional[str]


class PlainSecret(TypedDict):
    metadata: SecretMetadata
    value: str


class JsonSecret(TypedDict):
    metadata: SecretMetadata
    parsed: Dict[str, Any]


class DbSecret(TypedDict):
    metadata: SecretMetadata
    connection_string: str
    username: str
    password: str
    host: str
    port: Optional[int]
