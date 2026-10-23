from google.cloud import logging_v2
from google.cloud.logging_v2.proto import log_entry_pb2
from google.protobuf.timestamp_pb2 import Timestamp
from security_client import get_logging_client, PROJECT_ID
from security_models import KeyUsageSummaryResponse
import datetime

def summarize_key_usage(key_name_partial: str) -> KeyUsageSummaryResponse:
    client = get_logging_client()

    # In a real scenario, you would construct a more robust filter
    # and paginate through results. This is a simplified example.
    filter_str = f"resource.type=\"cloudkms_cryptokey\" AND resource.labels.cryptokey_id=\"{key_name_partial.split('/')[-1]}""
    entries = client.list_log_entries(
        resource_names=[f"projects/{PROJECT_ID}"],
        filter=filter_str,
        order_by=logging_v2.client.ListLogEntriesPager.DEFAULT_ORDER,
        page_size=100
    )

    encryption_ops = 0
    decryption_ops = 0
    sign_ops = 0
    verify_ops = 0
    last_event_timestamp = None

    for entry in entries:
        if entry.timestamp:
            event_time = entry.timestamp.ToDatetime()
            if last_event_timestamp is None or event_time > last_event_timestamp:
                last_event_timestamp = event_time

        if "protoPayload" in entry and entry.protoPayload.method_name:
            method_name = entry.protoPayload.method_name
            if "Encrypt" in method_name: # cloudkms.cryptokeys.encrypt
                encryption_ops += 1
            elif "Decrypt" in method_name: # cloudkms.cryptokeys.decrypt
                decryption_ops += 1
            elif "AsymmetricSign" in method_name: # cloudkms.cryptokeyVersions.asymmetricSign
                sign_ops += 1
            # Verification operations are typically client-side after public key retrieval
            # or could be custom methods logged. For simplicity, we're just counting signs.

    return KeyUsageSummaryResponse(
        key_name=key_name_partial,
        encryption_operations=encryption_ops,
        decryption_operations=decryption_ops,
        sign_operations=sign_ops,
        verify_operations=verify_ops, # KMS doesn't directly log a 'verify' op in the same way as sign/encrypt/decrypt
        last_event_timestamp=last_event_timestamp.isoformat() if last_event_timestamp else None
    )
