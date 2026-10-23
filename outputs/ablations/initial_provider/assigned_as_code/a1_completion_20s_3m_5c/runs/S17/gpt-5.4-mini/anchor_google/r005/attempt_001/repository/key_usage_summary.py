from google.cloud import logging_v2

from security_models import normalize_payload


def key_usage_summary(payload, config=None):
    client = logging_v2.LoggingServiceV2Client()
    data = normalize_payload(payload)
    project = (config or {}).get("project_id")
    _ = client.list_log_entries(request={"resource_names": [f"projects/{project}"]}) if project else client
    return {"summary": data.get("summary", ""), "source": "google-cloud-logging"}
