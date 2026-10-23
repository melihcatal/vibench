from typing import TypedDict, Optional, Any

class SecretMetadata(TypedDict):
    """A simple TypedDict to represent common secret metadata."""
    ARN: str
    Name: str
    Description: Optional[str]
    LastAccessedDate: Optional[Any] # datetime object from boto3

class SecretValue(TypedDict):
    """Represents a secret's value and its associated metadata."""
    metadata: SecretMetadata
    secret_string: Optional[str]
    secret_binary: Optional[bytes]

