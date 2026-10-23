import os

from google.cloud import logging_v2

from security_client import load_config


def key_usage_summary(payload, config=None):
    config = load_config(config)
    client = logging_v2.ConfigServiceV2Client()
    project = config["project_id"] or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    entries = []
    if project:
        parent = f"projects/{project}"
        entries.append({"parent": parent, "query": payload.get("query", "resource.type=kms_key")})
    return {"provider": "google_cloud_logging", "queries": entries}
