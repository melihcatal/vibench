from collections import Counter

from google.cloud import logging_v2

from security_models import normalize_text


def key_usage_summary(resource_name: str) -> dict:
    client = logging_v2.Client()
    entries = client.list_entries(filter_=f'resource.type="cloudkms_keyring" AND resource.labels.key_ring_id="{normalize_text(resource_name)}"')
    counts = Counter(entry.severity for entry in entries)
    return {"resource": normalize_text(resource_name), "event_counts": dict(counts), "provider": "google_cloud_logging"}
