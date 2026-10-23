import os
from typing import Dict, Any


def get_service_name() -> str:
    # Resolved via environment; for this demo we default to CloudWatch
    return "amazon-cloudwatch"


def build_client(service_name: str) -> Any:
    """Return a configured client for the Managed Log service."""
    if service_name == "amazon-cloudwatch":
        import boto3

        return boto3.client(
            "logs",
            region_name=os.getenv("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )
    raise NotImplementedError(f"Unsupported service: {service_name}")


def get_log_group() -> str:
    """Log group used for all interactions."""
    return os.getenv("LOG_GROUP_NAME", "/myapp/logs")


def normalize_payload(event: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a high‑level log event into the provider‑specific format."""
    return {
        "timestamp": event.get("time", int(event.get("timestamp", 0) / 1000)),
        "level": event.get("level", "INFO"),
        "message": event.get("msg"),
        "meta": event.get("meta", {}),
    }
