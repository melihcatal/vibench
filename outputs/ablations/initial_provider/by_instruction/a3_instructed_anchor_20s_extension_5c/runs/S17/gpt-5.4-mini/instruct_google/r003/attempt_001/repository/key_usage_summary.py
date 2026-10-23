from google.cloud import logging_v2


def key_usage_summary(project_id: str) -> dict:
    client = logging_v2.LoggingServiceV2Client()
    entries = list(client.list_log_entries(request={"resource_names": [f"projects/{project_id}"]}))
    return {"provider": "google_cloud_logging", "events": len(entries)}
