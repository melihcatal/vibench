import os
from typing import Dict, Any, Optional, List

from database_client import get_firestore_client
from database_models import DocumentRequest, normalize_response

# Import the SDK for the chosen text safety provider.
# Here we use AWS Bedrock Guardrails as an example.
from boto3 import client as boto3_client

safety_client = boto3_client(
    service_name="bedrock",
    region_name="us-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def check_text_safety(text: str) -> Optional[str]:
    """Call the safety provider and return a safety verdict.

    Returns None if safe, otherwise returns a reason string.
    """
    response = safety_client.invoke_model(
        ModelId="guardrails", Body=text.encode("utf-8")
    )
    verdict = response.get("body")
    if verdict == "safe":
        return None
    return verdict


def ensure_safe_fields(req: DocumentRequest) -> Dict[str, Any]:
    """Validate user‑generated text fields before storing.

    Args:
        req: DocumentRequest containing a payload dict.
    Returns:
        The sanitized payload, removing any unsafe fields.
    """
    safe_payload = {}
    for key, value in req.payload.items():
        if isinstance(value, str):
            if check_text_safety(value):
                raise ValueError(f"Unsafe content detected in field '{key}'")
        safe_payload[key] = value
    return safe_payload


def safe_upsert_document(req: DocumentRequest) -> str:
    """Upsert a document after passing safety checks.

    The operation mimics upsert_document but runs ensure_safe_fields first.
    """
    req.payload = ensure_safe_fields(req)
    return upsert_document(req)
