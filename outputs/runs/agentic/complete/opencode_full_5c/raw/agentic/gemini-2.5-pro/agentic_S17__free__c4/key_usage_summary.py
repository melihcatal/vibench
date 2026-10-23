import os
from google.cloud import logging_v2


def get_key_usage_summary():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    client = logging_v2.LoggingServiceV2Client()

    filter_str = (
        'resource.type="cloudkms_cryptokey" '
        'AND protoPayload.metadata.@type="type.googleapis.com/google.cloud.audit.AuditLog" '
        'AND protoPayload.methodName=("Encrypt" OR "Decrypt")'
    )

    entries = client.list_log_entries(
        resource_names=[f"projects/{project_id}"], filter_=filter_str, page_size=100
    )

    summary = {}
    for entry in entries:
        key_name = entry.resource.labels.get("key_id")
        method = entry.proto_payload.method_name
        if key_name not in summary:
            summary[key_name] = {"Encrypt": 0, "Decrypt": 0}
        if method in summary[key_name]:
            summary[key_name][method] += 1

    return summary
