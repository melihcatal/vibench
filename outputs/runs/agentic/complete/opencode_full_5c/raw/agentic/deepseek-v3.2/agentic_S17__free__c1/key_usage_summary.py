import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3 import types
from google.cloud import kms_v1


def summarize_key_usage(key_name: str, days: int = 7) -> Dict[str, Any]:
    """Summarize key usage and crypto events using Google Cloud Monitoring."""
    client = monitoring_v3.MetricServiceClient()
    kms_client = kms_v1.KeyManagementServiceClient()

    # Parse key name to get project ID
    parts = key_name.split("/")
    project_id = parts[1]

    # Get key metadata
    try:
        key_info = kms_client.get_crypto_key(request={"name": key_name})
        key_purpose = str(key_info.purpose).split(".")[-1]
        key_state = str(key_info.primary.state).split(".")[-1]
    except Exception as e:
        key_purpose = "UNKNOWN"
        key_state = "UNKNOWN"

    # Build time interval
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    interval = types.TimeInterval(
        {
            "end_time": {"seconds": int(end_time.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    # Query for encryption operations
    encryption_filter = f'metric.type="cloudkms.googleapis.com/crypto_key/operation_count" resource.label.crypto_key_id="{key_name.split("/")[-1]}" metric.label.operation="encrypt"'

    encryption_results = client.list_time_series(
        request={
            "name": f"projects/{project_id}",
            "filter": encryption_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    encryption_count = 0
    for series in encryption_results:
        for point in series.points:
            encryption_count += int(point.value.int64_value)

    # Query for decryption operations
    decryption_filter = f'metric.type="cloudkms.googleapis.com/crypto_key/operation_count" resource.label.crypto_key_id="{key_name.split("/")[-1]}" metric.label.operation="decrypt"'

    decryption_results = client.list_time_series(
        request={
            "name": f"projects/{project_id}",
            "filter": decryption_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    decryption_count = 0
    for series in decryption_results:
        for point in series.points:
            decryption_count += int(point.value.int64_value)

    # Query for signing operations
    signing_filter = f'metric.type="cloudkms.googleapis.com/crypto_key/operation_count" resource.label.crypto_key_id="{key_name.split("/")[-1]}" metric.label.operation="asymmetric_sign"'

    signing_results = client.list_time_series(
        request={
            "name": f"projects/{project_id}",
            "filter": signing_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    signing_count = 0
    for series in signing_results:
        for point in series.points:
            signing_count += int(point.value.int64_value)

    total_operations = encryption_count + decryption_count + signing_count

    # Get error metrics
    error_filter = f'metric.type="cloudkms.googleapis.com/crypto_key/operation_error_count" resource.label.crypto_key_id="{key_name.split("/")[-1]}"'

    error_results = client.list_time_series(
        request={
            "name": f"projects/{project_id}",
            "filter": error_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    error_count = 0
    for series in error_results:
        for point in series.points:
            error_count += int(point.value.int64_value)

    success_rate = 0
    if total_operations > 0:
        success_rate = ((total_operations - error_count) / total_operations) * 100

    return {
        "key_name": key_name,
        "provider": "google-cloud-kms",
        "monitoring_project": project_id,
        "period_days": days,
        "key_purpose": key_purpose,
        "key_state": key_state,
        "usage_summary": {
            "total_operations": total_operations,
            "encryption_operations": encryption_count,
            "decryption_operations": decryption_count,
            "signing_operations": signing_count,
            "error_count": error_count,
            "success_rate_percent": round(success_rate, 2),
        },
        "period": {
            "start": start_time.isoformat() + "Z",
            "end": end_time.isoformat() + "Z",
        },
    }


if __name__ == "__main__":
    # Example usage
    key_name = os.environ.get(
        "GCP_KMS_KEY_NAME",
        "projects/my-project/locations/global/keyRings/my-key-ring/cryptoKeys/my-key",
    )

    summary = summarize_key_usage(key_name, days=7)
    print(f"Key usage summary: {summary}")
