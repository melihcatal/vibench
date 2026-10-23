import os
import time
from typing import List
from google.cloud import monitoring_v3
from messaging_models import ProcessingResult


def summarize_processing(project_id: str, results: List[ProcessingResult]):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/messaging/processing_status"
    series.resource.type = "global"
    series.resource.labels["project_id"] = project_id

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)
    interval = monitoring_v3.TimeInterval(
        {"end_time": {"seconds": seconds, "nanos": nanos}}
    )

    successful = sum(1 for r in results if r.status == "success")
    failed = len(results) - successful

    # Metric for successful messages
    point_success = monitoring_v3.Point(
        {"interval": interval, "value": {"int64_value": successful}}
    )
    series.metric.labels["status"] = "success"
    series.points = [point_success]
    client.create_time_series(name=project_name, time_series=[series])

    # Metric for failed messages
    point_failed = monitoring_v3.Point(
        {"interval": interval, "value": {"int64_value": failed}}
    )
    series.metric.labels["status"] = "failed"
    series.points = [point_failed]
    client.create_time_series(name=project_name, time_series=[series])

    summary = f"Processing summary: {successful} successful, {failed} failed."
    print(summary)
    return summary


if __name__ == "__main__":
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not gcp_project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    results = [
        ProcessingResult(message_id="1", status="success"),
        ProcessingResult(
            message_id="2", status="failed", error_message="Invalid format"
        ),
        ProcessingResult(message_id="3", status="success"),
    ]
    summarize_processing(gcp_project_id, results)
