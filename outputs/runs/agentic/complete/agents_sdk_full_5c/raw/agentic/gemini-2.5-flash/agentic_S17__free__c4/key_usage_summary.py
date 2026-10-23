
"""
key_usage_summary.py - Summarize key usage and crypto events using Google Cloud Logging.
"""

from google.cloud import logging_v2 # Provider-identifying signal
from google.cloud.logging_v2.types import LogEntry
from security_models import KeyUsageSummaryResponse

def summarize_key_usage(project_id: str, days: int = 7) -> KeyUsageSummaryResponse:
    logging_client = logging_v2.LoggingServiceV2Client()

    # The Logging API hostname is logging.googleapis.com, implicitly used by the client.
    # Filter for KMS audit logs.
    filter_string = (
        f'resource.type="audited_resource" AND '
        f'protoPayload.serviceName="cloudkms.googleapis.com" AND '
        f'timestamp > "{(logging_client.timestamp_from_datetime(logging_client.now() - logging_client.timedelta(days=days))).isoformat()}" '
    )

    # Accumulators for different operation types
    encrypt_ops = 0
    decrypt_ops = 0
    sign_ops = 0

    # Iterate over log entries. This will paginate automatically.
    for entry in logging_client.list_log_entries(
        resource_names=[f"projects/{project_id}"],
        filter=filter_string,
        order_by=logging_v2.types.ListLogEntriesRequest.OrderBy.NEWEST,
    ):
        # Check protoPayload.methodName for specific KMS operations
        method_name = entry.proto_payload.method_name if hasattr(entry.proto_payload, 'method_name') else None

        if method_name == "google.cloud.kms.v1.KeyManagementService.Encrypt":
            encrypt_ops += 1
        elif method_name == "google.cloud.kms.v1.KeyManagementService.Decrypt":
            decrypt_ops += 1
        elif method_name == "google.cloud.kms.v1.KeyManagementService.AsymmetricSign":
            sign_ops += 1
        # Add other relevant KMS methods as needed, e.g., AsymmetricDecrypt, MacSign, MacVerify

    return KeyUsageSummaryResponse(total_encrypt_ops=encrypt_ops, total_decrypt_ops=decrypt_ops, total_sign_ops=sign_ops)
