import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from google.cloud import pubsub_v1
from google.cloud import monitoring_v3


def summarize_message_processing(
    topic_id: str, time_range_hours: int = 24
) -> Dict[str, Any]:
    """Summarize message processing results using Google Cloud Monitoring."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")

    client = monitoring_v3.MetricServiceClient()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=time_range_hours)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(end_time.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    results = {
        "topic": f"projects/{project_id}/topics/{topic_id}",
        "time_range": {
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "hours": time_range_hours,
        },
        "metrics": {},
        "provider": "google-cloud-monitoring",
    }

    metric_types = [
        "pubsub.googleapis.com/topic/send_request_count",
        "pubsub.googleapis.com/topic/send_message_operations_count",
        "pubsub.googleapis.com/topic/byte_cost",
        "pubsub.googleapis.com/subscription/num_undelivered_messages",
        "pubsub.googleapis.com/subscription/pull_message_operations_count",
    ]

    for metric_type in metric_types:
        request = monitoring_v3.ListTimeSeriesRequest(
            name=f"projects/{project_id}",
            filter=f'metric.type="{metric_type}" AND resource.label.topic_id="{topic_id}"',
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        try:
            time_series = client.list_time_series(request=request)
            series_list = list(time_series)

            if series_list:
                metric_name = metric_type.split("/")[-1]
                latest_point = (
                    series_list[0].points[-1] if series_list[0].points else None
                )

                if latest_point:
                    results["metrics"][metric_name] = {
                        "value": latest_point.value.double_value
                        if hasattr(latest_point.value, "double_value")
                        else latest_point.value.int64_value,
                        "timestamp": latest_point.interval.end_time.ToDatetime().isoformat(),
                    }
        except Exception as e:
            results["metrics"][metric_type.split("/")[-1]] = {"error": str(e)}

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    try:
        topic_stats = publisher.get_topic(request={"topic": topic_path})
        results["topic_info"] = {
            "name": topic_stats.name,
            "labels": dict(topic_stats.labels) if topic_stats.labels else {},
            "message_retention_duration": str(topic_stats.message_retention_duration),
        }
    except Exception as e:
        results["topic_info"] = {"error": str(e)}

    subscriber = pubsub_v1.SubscriberClient()

    try:
        subscriptions = []
        for subscription in subscriber.list_subscriptions(
            request={"project": f"projects/{project_id}"}
        ):
            if subscription.topic == topic_path:
                sub_stats = subscriber.get_subscription(
                    request={"subscription": subscription.name}
                )
                subscriptions.append(
                    {
                        "name": sub_stats.name.split("/")[-1],
                        "ack_deadline_seconds": sub_stats.ack_deadline_seconds,
                        "message_retention_duration": str(
                            sub_stats.message_retention_duration
                        ),
                        "retry_policy": {
                            "minimum_backoff": str(
                                sub_stats.retry_policy.minimum_backoff
                            )
                            if sub_stats.retry_policy
                            else None,
                            "maximum_backoff": str(
                                sub_stats.retry_policy.maximum_backoff
                            )
                            if sub_stats.retry_policy
                            else None,
                        }
                        if sub_stats.retry_policy
                        else None,
                    }
                )
        results["subscriptions"] = subscriptions
    except Exception as e:
        results["subscriptions"] = {"error": str(e)}

    results["summary"] = {
        "total_send_requests": results["metrics"]
        .get("send_request_count", {})
        .get("value", 0),
        "total_messages_sent": results["metrics"]
        .get("send_message_operations_count", {})
        .get("value", 0),
        "total_byte_cost": results["metrics"].get("byte_cost", {}).get("value", 0),
        "undelivered_messages": results["metrics"]
        .get("num_undelivered_messages", {})
        .get("value", 0),
        "pull_operations": results["metrics"]
        .get("pull_message_operations_count", {})
        .get("value", 0),
        "subscription_count": len(results.get("subscriptions", [])),
        "processing_efficiency": calculate_efficiency(results),
    }

    return results


def calculate_efficiency(metrics_data: Dict[str, Any]) -> Dict[str, float]:
    """Calculate processing efficiency metrics."""
    efficiency = {}

    send_requests = (
        metrics_data["metrics"].get("send_request_count", {}).get("value", 0)
    )
    messages_sent = (
        metrics_data["metrics"].get("send_message_operations_count", {}).get("value", 0)
    )
    pull_ops = (
        metrics_data["metrics"].get("pull_message_operations_count", {}).get("value", 0)
    )
    undelivered = (
        metrics_data["metrics"].get("num_undelivered_messages", {}).get("value", 0)
    )

    if send_requests > 0:
        efficiency["messages_per_request"] = (
            messages_sent / send_requests if send_requests > 0 else 0
        )

    if messages_sent > 0:
        efficiency["undelivered_percentage"] = (
            (undelivered / messages_sent * 100) if messages_sent > 0 else 0
        )

    if pull_ops > 0:
        efficiency["messages_per_pull"] = (
            messages_sent / pull_ops if pull_ops > 0 else 0
        )

    return efficiency


def get_subscription_backlog(subscription_id: str) -> Dict[str, Any]:
    """Get subscription backlog information."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")

    client = monitoring_v3.MetricServiceClient()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": int(end_time.timestamp())},
            "start_time": {"seconds": int(start_time.timestamp())},
        }
    )

    request = monitoring_v3.ListTimeSeriesRequest(
        name=f"projects/{project_id}",
        filter=f'metric.type="pubsub.googleapis.com/subscription/num_undelivered_messages" AND resource.label.subscription_id="{subscription_id}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    try:
        time_series = client.list_time_series(request=request)
        series_list = list(time_series)

        if series_list and series_list[0].points:
            latest_point = series_list[0].points[-1]
            backlog = (
                latest_point.value.double_value
                if hasattr(latest_point.value, "double_value")
                else latest_point.value.int64_value
            )

            return {
                "subscription_id": subscription_id,
                "backlog_messages": backlog,
                "timestamp": latest_point.interval.end_time.ToDatetime().isoformat(),
                "provider": "google-cloud-monitoring",
            }
    except Exception as e:
        return {
            "subscription_id": subscription_id,
            "error": str(e),
            "provider": "google-cloud-monitoring",
        }

    return {
        "subscription_id": subscription_id,
        "backlog_messages": 0,
        "provider": "google-cloud-monitoring",
    }


if __name__ == "__main__":
    summary = summarize_message_processing("event-topic", time_range_hours=1)
    print(f"Message processing summary: {json.dumps(summary, indent=2)}")
