import json
from security_client import SecurityClient
from security_models import ResponsePayload


def rotation_summary(secret_name: str, stage: str = "AWSCURRENT") -> str:
    client = SecurityClient()
    # Placeholder: in practice retrieve the secret with version stage
    raw = {
        "value": f"rotated-value-{stage}-{secret_name}",
        "metadata": {"stage": stage, "timestamp": "2025-01-01T00:00:00Z"},
    }
    # Determine if rotation is pending or successful
    if stage == "AWSPREVIOUS":
        status = "Pending rotation"
    else:
        status = "Rotation complete"
    return f"Secret {secret_name} [{stage}] - {status}"
