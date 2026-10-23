# SAME-SCENARIO: aggregate_metric_stats.py
from observability_client import MetricsClient
from observability_models import MetricStatsRequest, AggregationType

def aggregate_metric_stats(metric_name: str, start_timestamp: str, end_timestamp: str, granularity: str = "1m") -> dict:
    request = MetricStatsRequest(
        metric=metric_name,
        start=start_timestamp,
        end=end_timestamp,
        granularity=granularity,
        aggregations=[
            AggregationType.AVG,
            AggregationType.MAX,
            AggregationType.MIN,
            AggregationType.SUM,
        ],
    )
    return MetricsClient.get().aggregate(request)

if __name__ == "__main__":
    # Example using Google Cloud Monitoring (set GOOGLE_APPLICATION_CREDENTIALS)
    print(aggregate_metric_stats("compute.googleapis.com/instance/cpu/utilization", "2025-08-01T12:00:00Z", "2025-08-01T13:00:00Z"))
