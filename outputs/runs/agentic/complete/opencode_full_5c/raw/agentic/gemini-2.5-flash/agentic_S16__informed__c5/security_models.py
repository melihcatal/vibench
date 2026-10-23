import json
from typing import Dict, Any, Optional


class Secret:
    def __init__(self, name: str, value: Any, version_id: Optional[str] = None):
        self.name = name
        self.value = value
        self.version_id = version_id

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "value": self.value, "version_id": self.version_id}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Secret":
        return cls(
            name=data["name"], value=data["value"], version_id=data.get("version_id")
        )


class ApiKeySecret(Secret):
    def __init__(self, name: str, key: str, version_id: Optional[str] = None):
        super().__init__(name, key, version_id)
        self.key = key

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "key": self.key, "version_id": self.version_id}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ApiKeySecret":
        return cls(
            name=data["name"], key=data["key"], version_id=data.get("version_id")
        )


class DatabaseSecret(Secret):
    def __init__(
        self,
        name: str,
        username: str,
        password: str,
        host: str,
        port: int,
        dbname: str,
        version_id: Optional[str] = None,
    ):
        super().__init__(
            name,
            {
                "username": username,
                "password": password,
                "host": host,
                "port": port,
                "dbname": dbname,
            },
            version_id,
        )
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "host": self.host,
            "port": self.port,
            "dbname": self.dbname,
            "version_id": self.version_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DatabaseSecret":
        return cls(
            name=data["name"],
            username=data["username"],
            password=data["password"],
            host=data["host"],
            port=data["port"],
            dbname=data["dbname"],
            version_id=data.get("version_id"),
        )


class JsonSecret(Secret):
    def __init__(
        self, name: str, json_data: Dict[str, Any], version_id: Optional[str] = None
    ):
        super().__init__(name, json_data, version_id)
        self.json_data = json_data

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "json_data": self.json_data,
            "version_id": self.version_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JsonSecret":
        return cls(
            name=data["name"],
            json_data=data["json_data"],
            version_id=data.get("version_id"),
        )
