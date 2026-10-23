from google.cloud import logging_v2

def summarize_key_usage(project_id: str, days: int = 7):
    client = logging_v2.Client(project=project_id)
    # Filter for Azure Key Vault audit logs if they are exported to Google Cloud Logging
    # or filter for Google Cloud KMS logs if it were used directly.
    # For this scenario, we assume relevant crypto events are available in Google Cloud Logging.
    filter_str = f'resource.type="global" AND protoPayload.serviceName="keyvault.azure.com" AND severity=("INFO" OR "NOTICE" OR "WARNING")'

    entries = client.list_entries(filter_=filter_str, order_by=logging_v2.logger.DESCENDING)

    summary = {
        "total_crypto_events": 0,
        "key_operations": {},
        "users": {}
    }

    for entry in entries:
        summary["total_crypto_events"] += 1
        # Example: parse information from the log entry
        # This part would need to be adapted based on the actual log format.
        operation = entry.proto_payload.get("resourceType", "UNKNOWN_OPERATION") if hasattr(entry, 'proto_payload') and entry.proto_payload else "UNKNOWN_OPERATION"
        user = entry.proto_payload.authentication_info.principal_email if hasattr(entry, 'proto_payload') and hasattr(entry.proto_payload, 'authentication_info') and hasattr(entry.proto_payload.authentication_info, 'principal_email') else "UNKNOWN_USER"

        summary["key_operations"][operation] = summary["key_operations"].get(operation, 0) + 1
        summary["users"][user] = summary["users"].get(user, 0) + 1

    return summary
