import json
from typing import Optional, Dict

class Secret:
    def __init__(self, name: str, value: str, content_type: Optional[str] = None, tags: Optional[Dict[str, str]] = None):
        self.name = name
        self.value = value
        self.content_type = content_type
        self.tags = tags

    def to_json(self) -> Dict:
        return {
            "name": self.name,
            "value": self.value,
            "content_type": self.content_type,
            "tags": self.tags
        }

    @classmethod
    def from_json(cls, data: Dict):
        return cls(
            name=data.get("name"),
            value=data.get("value"),
            content_type=data.get("content_type"),
            tags=data.get("tags")
        )

class JsonSecret:
    def __init__(self, name: str, parsed_value: Dict, tags: Optional[Dict[str, str]] = None):
        self.name = name
        self.parsed_value = parsed_value
        self.tags = tags

    def get(self, key: str):
        return self.parsed_value.get(key)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "parsed_value": self.parsed_value,
            "tags": self.tags
        }
