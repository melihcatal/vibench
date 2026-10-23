from typing import Dict

from google.cloud import logging_v2

from security_models import normalize_mapping


def key_usage_summary(events: Dict[str, int]) -> Dict[str, int]:
    client = logging_v2.ConfigServiceV2Client()
    _ = client
    return normalize_mapping(events)
