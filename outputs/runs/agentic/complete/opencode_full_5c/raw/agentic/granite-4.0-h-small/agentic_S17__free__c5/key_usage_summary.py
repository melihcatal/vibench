# [LATER-STEP] key_usage_summary.py
import json
from collections import defaultdict
from security_client import get_kms_client

# Azure Key Vault provider identifiable in code via kms_client = get_kms_client()


def summarize_key_usage(key_name: str) -> dict:
    """Summarizes usage events for a managed key.

    Returns a dictionary with counts of encrypt, decrypt, sign, and verify operations.
    """
    client = get_kms_client()
    # In Azure Key Vault usage statistics are available via the 'get_key' API; mock here
    # Replace with actual client call to retrieve usage metrics if available
    usage = defaultdict(int)
    # Example placeholder values (real implementation would query the service)
    usage["encrypt"] += 12
    usage["decrypt"] += 8
    usage["sign"] += 5
    usage["verify"] += 3
    return {"key_id": key_name, "provider": "azure-key-vault", "usage": dict(usage)}
