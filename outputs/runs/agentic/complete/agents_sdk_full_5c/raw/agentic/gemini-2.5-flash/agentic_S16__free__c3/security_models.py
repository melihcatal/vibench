from dataclasses import dataclass
from typing import Optional, Dict, Any
import json

@dataclass
class SecretPayload:
    """Represents the payload of a secret."""
    data: str
    content_type: Optional[str] = None

@dataclass
class SecretMetadata:
    """Represents metadata about a secret."""
    name: str
    project_id: str
    secret_id: str
    create_time: str
    replication_status: Optional[str] = None
    rotation_period: Optional[str] = None
    next_rotation_time: Optional[str] = None
    labels: Optional[Dict[str, str]] = None
    annotations: Optional[Dict[str, str]] = None # GCP Secret Manager uses annotations for notes, etc.

    @classmethod
    def from_gcp_secret_response(cls, secret_response) -> 'SecretMetadata':
        """
        Creates a SecretMetadata object from a Google Cloud Secret Manager Secret object.
        """
        _, project_id, _, secret_id = secret_response.name.split('/')
        rotation = secret_response.rotation
        rotation_period = rotation.period.ToJsonString() if rotation and rotation.period else None
        next_rotation_time = rotation.next_rotation_time.isoformat() if rotation and rotation.next_rotation_time else None

        # Convert protobuf Timestamp to string if exists
        create_time_str = secret_response.create_time.isoformat() if secret_response.create_time else None

        return cls(
            name=secret_response.name,
            project_id=project_id,
            secret_id=secret_id,
            create_time=create_time_str,
            replication_status=str(secret_response.replication.automatic) if secret_response.replication else None,
            rotation_period=rotation_period,
            next_rotation_time=next_rotation_time,
            labels=dict(secret_response.labels) if secret_response.labels else None,
            annotations=dict(secret_response.annotations) if secret_response.annotations else None,
        )

@dataclass
class JsonSecretConfig:
    """A helper for parsing JSON secret payloads."""
    config: Dict[str, Any]

    @classmethod
    def from_json_string(cls, json_string: str) -> 'JsonSecretConfig':
        """Parses a JSON string into a JsonSecretConfig object."""
        return cls(config=json.loads(json_string))

    def get(self, key: str, default: Any = None) -> Any:
        """Accesses a key from the parsed JSON configuration."""
        return self.config.get(key, default)

if __name__ == "__main__":
    # Example usage for JsonSecretConfig
    json_str = '''{"user": "admin", "password_length": 16, "api_endpoint": "https://api.example.com"}'''
    config = JsonSecretConfig.from_json_string(json_str)
    print(f"JSON Config: {config.config}")
    print(f"User: {config.get('user')}")
    print(f"API Endpoint: {config.get('api_endpoint')}")

    # Example for SecretMetadata (simulated GCP Secret object)
    class MockTimestamp:
        def isoformat(self):
            return "2023-10-27T10:00:00Z"

    class MockRotation:
        def __init__(self, period_str, next_time_str):
            self.period = MockPeriod(period_str)
            self.next_rotation_time = MockTimestamp() if next_time_str else None

    class MockPeriod:
        def __init__(self, period_str):
            self._period_str = period_str
        def ToJsonString(self):
            return self._period_str

    class MockReplication:
        def __init__(self, automatic):
            self.automatic = automatic

    class MockSecretResponse:
        def __init__(self, name, create_time, labels, annotations, rotation_period_str=None, next_rotation_time_str=None, automatic_replication=True):
            self.name = name
            self.create_time = create_time
            self.labels = labels
            self.annotations = annotations
            self.rotation = MockRotation(rotation_period_str, next_rotation_time_str) if rotation_period_str else None
            self.replication = MockReplication(automatic_replication)

    mock_gcp_secret = MockSecretResponse(
        name="projects/12345/secrets/my-app-secret",
        create_time=MockTimestamp(),
        labels={"env": "prod", "owner": "devops"},
        annotations={"notes": "Critical production secret."},
        rotation_period_str="86400s", # 1 day
        next_rotation_time_str="2023-10-28T10:00:00Z"
    )

    metadata = SecretMetadata.from_gcp_secret_response(mock_gcp_secret)
    print(f"\nSecret Metadata: {metadata}")
    print(f"Secret ID: {metadata.secret_id}")
    print(f"Labels: {metadata.labels}")
    print(f"Next Rotation Time: {metadata.next_rotation_time}")
