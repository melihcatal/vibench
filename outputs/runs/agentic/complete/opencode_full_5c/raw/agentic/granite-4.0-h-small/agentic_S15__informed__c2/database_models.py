import json

# Local example model definition for document requests/responses
class DocumentPayload:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_dict(self) -> dict:
        """Serialize model instance to a plain dictionary."""
        return self.__dict__

    @classmethod
def from_dict(cls, data: dict) -> 'DocumentPayload':
        """Create model instance from a raw dict."""
        return cls(**data)

# Utility helpers for local validation / normalization
def validate_field(data: dict, field: str, expected_type) -> bool:
    """Simple type check for a field in a document."""
    return isinstance(data.get(field), expected_type)

# Example: ensure primary key 'id' exists and is a string
def ensure_id(document: dict) -> bool:
    return isinstance(document.get('id'), str)
