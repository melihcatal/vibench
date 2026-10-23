from google.cloud import monitoring_v3
import os


def summarize_message_processing(results, config=None):
    config = config or {}
    project_id = config.get("project_id", os.getenv("GOOGLE_CLOUD_PROJECT"))

    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    # In a real scenario, you would send detailed metrics here.
    # For this example, we'll just return a simple summary of the results.
    # Example of a metric write would involve creating TimeSeries objects.

    successful_messages = sum(1 for r in results if "error" not in r)
    failed_messages = len(results) - successful_messages

    summary = {
        "total_messages_processed": len(results),
        "successful_messages": successful_messages,
        "failed_messages": failed_messages,
    }
    
    # Example of how to create a metric descriptor and write time series (simplified)
    # This part is illustrative as creating full time series involves more setup
    # For now, we'll just return the summary dict.

    # series = monitoring_v3.TimeSeries()
    # series.metric.type = "custom.googleapis.com/message_processor/summary"
    # series.resource.type = "global"
    # point = monitoring_v3.Point()
    # point.value.int64_value = successful_messages
    # now = time.time()
    # point.interval.end_time.seconds = int(now)
    # point.interval.end_time.nanos = int((now - int(now)) * 10**9)
    # series.points.append(point)
    # client.create_time_series(name=project_name, time_series=[series])

    return summary
