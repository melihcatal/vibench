import os
import re
from local_helpers.observability_client import get_client
from local_helpers.observability_models import MetricQueryRequest, MetricDataResult
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("METRICS_PROVIDER", "AZURE_MONITOR")  # default provider

# Simple regex for unsafe characters in metric labels (e.g., scripts, HTML tags)
UNSAFE_PATTERN = re.compile(r'[<>"&\\]')


def check_unsafe_labels(labels: dict) -> List[str]:
    """
    Inspect a dict of metric label/value pairs and return a list of label names that contain unsafe
    characters (HTML/JS script tags, angle brackets, ampersand, backslash). This catches potentially
    malicious or malformed text that could be used in XSS or injection contexts.
    """
    unsafe = []
    for label, value in labels.items():
        if isinstance(value, str) and UNSAFE_PATTERN.search(value):
            unsafe.append(label)
    return unsafe


def safety_check_metric_labels(
    resource_id: str, metric_name: str, start_time: str, end_time: str
):
    """
    Query metric data with its label set and inspect each label for unsafe content.
    The provider client must return the raw label dictionary for each metric point.
    """
    client = get_client(PROVIDER)
    # Query a recent datapoint to retrieve the label set
    request = MetricQueryRequest(
        resource_id=resource_id,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        interval="PT1M",
        aggregation="Average",
        filter=None,
    )
    response = client.query_metric_window(
        resource_id, metric_name, start_time, end_time
    )
    # Assume response contains a list of datapoints with a 'labels' field
    unsafe_labels = []
    for dp in response.get("datapoints", []):
        unsafe_labels.extend(check_unsafe_labels(dp.get("labels", {})))
    return {
        "unsafe_labels": unsafe_labels,
        "resource": resource_id,
        "metric": metric_name,
    }


if __name__ == "__main__":
    # Demo (real usage would integrate with monitoring pipelines)
    print(
        json.dumps(
            safety_check_metric_labels(
                "my-resource",
                "errorRate",
                "2024-01-01T00:00:00Z",
                "2024-01-02T00:00:00Z",
            ),
            indent=2,
        )
    )
