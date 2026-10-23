import json
from typing import Dict, Any, Optional

class Secret:
    def __init__(self, name: str, arn: str, secret_string: Optional[str] = None, secret_binary: Optional[bytes] = None):
        self.name = name
        self.arn = arn
        self.secret_string = secret_string
        self.secret_binary = secret_binary

    def get_string_value(self) -> Optional[str]:
        return self.secret_string

    def get_json_value(self) -> Optional[Dict[str, Any]]:
        if self.secret_string:
            try:
                return json.loads(self.secret_string)
            except json.JSONDecodeError:
                return None
        return None

class SecretVersion:
    def __init__(self, version_id: str, secret_string: Optional[str] = None, secret_binary: Optional[bytes] = None, stages: list[str] = None):
        self.version_id = version_id
        self.secret_string = secret_string
        self.secret_binary = secret_binary
        self.stages = stages if stages is not None else []

    def get_string_value(self) -> Optional[str]:
        return self.secret_string

    def get_json_value(self) -> Optional[Dict[str, Any]]:
        if self.secret_string:
            try:
                return json.loads(self.secret_string)
            except json.JSONDecodeError:
                return None
        return None
