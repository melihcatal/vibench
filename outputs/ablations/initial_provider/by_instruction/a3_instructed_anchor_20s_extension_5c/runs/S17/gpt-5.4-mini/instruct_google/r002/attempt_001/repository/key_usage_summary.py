from google.cloud import logging_v2

from security_client import load_security_config


def key_usage_summary() -> str:
    config = load_security_config()
    client = logging_v2.ConfigServiceV2Client()
    return f"{config.project_id}:{config.crypto_key}:{client.transport.__class__.__name__}"
