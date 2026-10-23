import datetime
from google.cloud import logging as cloud_logging
from security_client import SecurityClientConfig, LoggingClientWrapper

def summarize_key_usage(project_id: str, key_id: str, days: int = 7) -> list[dict]:
    """Summarizes key usage and crypto events for a given key using Google Cloud Logging.

    Args:
        project_id: Your Google Cloud project ID.
        key_id: The ID of the key to summarize usage for.
        days: The number of past days to check for logs.

    Returns:
        A list of dictionaries, each representing a key usage event.
    """
    client_wrapper = LoggingClientWrapper()
    logging_client = client_wrapper.client

    # Calculate the time range for the logs
    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(days=days)

    # Filter for KMS audit logs related to the specific key
    # resource.type="k8s_container" is wrong, it should be something like resource.type="cloudkms_cryptokey"
    # Let's correct the filter to target KMS audit logs and the specific key resource
    filter_string = (
        f'resource.type="cloudkms_cryptokey" AND '
        f'resource.labels.crypto_key_id="{key_id}" AND '
        f'timestamp>="{start_time.isoformat()}" AND '
        f'timestamp<="{end_time.isoformat()}"'
    )

    entries = logging_client.list_entries(filter_=filter_string, project_ids=[project_id])

    summary = []
    for entry in entries:
        # Extract relevant information from the log entry
        event = {
            "timestamp": entry.timestamp.isoformat(),
            "severity": entry.severity,
            "log_name": entry.log_name,
            "method_name": None,
            "principal_email": None,
            "resource_name": None,
        }

        if entry.proto_payload and entry.proto_payload.HasField('audit_log'):
            audit_log = entry.proto_payload.audit_log
            event["method_name"] = audit_log.method_name
            event["principal_email"] = audit_log.authentication_info.principal_email
            if audit_log.resource_name:
                event["resource_name"] = audit_log.resource_name

        summary.append(event)

    return summary
