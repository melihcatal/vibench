from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class SecretPayload:
    data: bytes
    data_crc32c: Optional[int] = None


@dataclass
class SecretVersion:
    name: str
    state: str
    create_time: Any
    destroy_time: Optional[Any] = None
    replication_status: Optional[Any] = None


@dataclass
class Secret:
    name: str
    labels: Dict[str, str] = field(default_factory=dict)
    create_time: Optional[Any] = None
    replication: Optional[Any] = None
    rotation: Optional[Any] = None
    expire_time: Optional[Any] = None
    version_aliases: Dict[str, str] = field(default_factory=dict)
    etag: Optional[str] = None
    customer_managed_key: Optional[Any] = None


@dataclass
class ParsedJsonSecret:
    key: str
    value: Any
