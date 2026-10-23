from typing import TypedDict, Any


class DbSecret(TypedDict):
    username: str
    password: str
    host: str
    dbname: str
    port: int


class JsonSecret(TypedDict):
    key: str
    value: Any


class SecretVersionInfo(TypedDict):
    id: str
    version_id: str
    created_at: str
    payload: str
