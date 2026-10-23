from google.cloud import logging_v2
from google.cloud.logging_v2.proto import log_entry_pb2
from google.cloud.monitoring_v3 import MetricServiceClient
from google.cloud.monitoring_v3.types import TimeInterval, ListTimeSeriesRequest, Aggregation
from datetime import datetime, timedelta
import os

def summarize_kms_key_usage(project_id: str, days: int = 7):
    """Summarizes Google Cloud KMS key usage and crypto events from audit logs and monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        days: The number of days to look back for events.

    Returns:
        A dictionary containing a summary of key usage.
    """
    logging_client = logging_v2.LoggingServiceV2Client()
    monitoring_client = MetricServiceClient()

    project_name = f"projects/{project_id}"

    # Summarize audit logs for KMS key usage
    log_filter = f'resource.type="cloudkms_cryptokey" AND protoPayload.serviceName="cloudkms.googleapis.com" AND severity=INFO AND timestamp>="{(datetime.now() - timedelta(days=days)).isoformat()}"'
    
    log_entries_summary = {}
    for entry in logging_client.list_log_entries(resource_names=[project_name], filter=log_filter):
        method_name = entry.proto_payload.method_name if entry.proto_payload else "UNKNOWN"
        resource_name = entry.resource.labels.get("crypto_key_id", "UNKNOWN")

        if resource_name not in log_entries_summary:
            log_entries_summary[resource_name] = {}
        log_entries_summary[resource_name][method_name] = log_entries_summary[resource_name].get(method_name, 0) + 1

    # Summarize monitoring metrics for key operations (e.g., encryption operations)
    interval = TimeInterval(
        end_time=datetime.now(),
        start_time=datetime.now() - timedelta(days=days)
    )

    # Example metric: cloudkms.googleapis.com/crypto_key/encrypt_operations
    metric_filter = f'metric.type="cloudkms.googleapis.com/crypto_key/encrypt_operations" AND resource.labels.project_id="{project_id}"'
    
    # Using a simple aggregation for demonstration
    aggregation = Aggregation(
        alignment_period={"seconds": 3600}, # 1 hour
        per_series_aligner=Aggregation.Aligner.ALIGN_SUM,
        cross_series_reducer=Aggregation.Reducer.REDUCE_SUM,
        group_by_fields=["resource.label.crypto_key_id"]
    )

    metric_results_summary = {}
    try:
        for response in monitoring_client.list_time_series(request=ListTimeSeriesRequest(
            name=project_name,
            filter=metric_filter,
            interval=interval,
            view=ListTimeSeriesRequest.TimeSeriesView.FULL,
            aggregation=aggregation
        )):
            for series in response.time_series:
                key_id = series.resource.labels.get("crypto_key_id", "UNKNOWN")
                total_value = sum(p.value.int64_value for p in series.points)
                metric_results_summary[key_id] = metric_results_summary.get(key_id, 0) + total_value
    except Exception as e:
        # Handle cases where the metric might not exist or permission issues
        print(f"Could not retrieve monitoring metrics: {e}")

    return {
        "audit_logs": log_entries_summary,
        "monitoring_metrics": metric_results_summary
    }
