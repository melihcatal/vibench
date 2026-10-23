import os
from typing import Dict, Iterable

from security_client import get_secret_manager_client

# Google Cloud Secret Manager provider signal
from google.cloud import secretmanager


def secret_label_safety(labels: Dict[str, str]) -> Dict[str, bool]:
    unsafe_tokens = {"password", "token", "prod", "secret", "private", "key"}
    return {k: not any(token in f"{k} {v}".lower() for token in unsafe_tokens) for k, v in labels.items()}
