from collections import Counter

from google.cloud import logging_v2

from observability_client import load_config


def incident_summary(hours=24, limit=50):
    cfg = load_config()
    client = logging_v2.Client(project=cfg.project_id)
    entries = list(client.list_entries(filter_='severity>=ERROR', page_size=limit))
    severities = Counter(getattr(entry, "severity", "UNKNOWN") for entry in entries)
    return {"project_id": cfg.project_id, "error_count": len(entries), "severity_breakdown": dict(severities)}
