import json
from typing import Dict, Any, Optional


class SecretValue:
    """Represents a secret value fetched from a secret manager."""

    def __init__(self, name: str, value: str, version: str = "latest"):
        self.name = name
        self.value = value
        self.version = version

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "value": self.value, "version": self.version}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SecretValue":
        return cls(data["name"], data["value"], data.get("version", "latest"))


class DatabaseSecret(SecretValue):
    """Represents a database connection secret."""

    def __init__(
        self,
        name: str,
        username: str,
        password: str,
        host: str,
        port: int,
        database: str,
    ):
        super().__init__(
            name,
            json.dumps(
                {
                    "username": username,
                    "password": password,
                    "host": host,
                    "port": port,
                    "database": database,
                }
            ),
        )
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    @classmethod
    def from_json_string(cls, name: str, json_string: str) -> "DatabaseSecret":
        data = json.loads(json_string)
        return cls(
            name,
            data["username"],
            data["password"],
            data["host"],
            data["port"],
            data["database"],
        )


class JsonSecret(SecretValue):
    """Represents a JSON-formatted secret."""

    def __init__(self, name: str, json_data: Dict[str, Any]):
        super().__init__(name, json.dumps(json_data))
        self.json_data = json_data

    @classmethod
    def from_json_string(cls, name: str, json_string: str) -> "JsonSecret":
        data = json.loads(json_string)
        return cls(name, data)
