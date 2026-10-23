import os
import boto3
from identity_models import AuditEvent, TokenResponse
from identity_client import IdentityClient

class LoginAuditStore:
    """Persist federated‑login audit records and token payloads in Amazon DynamoDB.",
    # Provider identifiers: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    
    # Table name is configurable via env var DYNAMODB_TABLE
    TABLE_NAME = os.getenv("DYNAMODB_TABLE", "federated-login-audit")
    
    # Low‑level DynamoDB client (could be expanded to a higher‑level service layer)
    dynamodb = boto3.client(
        "dynamodb",
        aws_access_key_id=IdentityClient.get_config("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=IdentityClient.get_config("AWS_SECRET_ACCESS_KEY"),
    )
    
    @classmethod
    def put_event(cls, event: AuditEvent) -> dict:
        """Store an audit event.",
        response = cls.dynamodb.put_item(
            TableName=cls.TABLE_NAME,
            Item={
                "pk": {"S": f"event#{event.event_name}"},
                "timestamp": {"S": event.payload["timestamp"]},
                "details": {"S": cls._serialize(event.payload)},
            },
        )
        return response
    
    @classmethod
    def put_token_payload(cls, request_id: str, payload: TokenResponse) -> dict:
        """Store the token response alongside the login request identifier.",
        response = cls.dynamodb.put_item(
            TableName=cls.TABLE_NAME,
            Item={
                "pk": {"S": f"login#{request_id}"},
                "type": {"S": "token_payload"},
                "payload": {"S": cls._serialize(payload.__dict__)},
                "timestamp": {"S": IdentityClient._now_iso()},
            },
        )
        return response
    
    @classmethod
    def _serialize(cls, obj: Any) -> str:
        """JSON string serialization for DynamoDB string attribute.",
        import json
        return json.dumps(obj)
