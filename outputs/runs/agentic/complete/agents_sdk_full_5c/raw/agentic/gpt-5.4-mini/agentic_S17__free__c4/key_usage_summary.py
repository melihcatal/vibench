from __future__ import annotations

from security_client import SecurityClient

# Google Cloud KMS managed key usage summary.

def key_usage_summary(key_name: str, labels=None):
    client = SecurityClient()
    return client.summarize_usage(key_name, labels=labels)
