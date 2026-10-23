import dataclasses
import typing

@dataclasses.dataclass
class SecretPayload:
    secret_name: str
    version_id: typing.Optional[str] = None
    key_field: typing.Optional[str] = None

@dataclasses.dataclass
class DbSecret:
    username: str
    password: str
    host: str
    port: typing.Optional[int] = None
    database: typing.Optional[str] = None

@dataclasses.dataclass
class ApiKeySecret:
    api_key: str

@dataclasses.dataclass
class SecretMetadata:
    secret_name: str
    version: str
    enabled: bool
    created_on: typing.Optional[typing.Any] = None # datetime object
    expires_on: typing.Optional[typing.Any] = None # datetime object
    tags: typing.Optional[typing.Dict[str, str]] = None
