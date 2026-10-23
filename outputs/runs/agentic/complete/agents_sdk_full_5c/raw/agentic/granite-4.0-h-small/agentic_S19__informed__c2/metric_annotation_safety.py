import os
import requests
from observability_client import get_cloudwatch_client
from observability_models import MetricStatisticsRequest

def check_annotations_safe(namespace, metric_name, start_time, end_time, unsafe_keywords=None):
    """Check free‑text metric labels or annotations for unsafe text using Perspective API (REST)."
    if unsafe_keywords is None:
        unsafe_keywords = ["hate", "harass", "violence", "self‑harm"]
    # Retrieve existing metric definitions (labels) via CloudWatch DescribeAlarms or GetMetricWidgetImage;
    # for simplicity we just query a dummy statistic to trigger credentials, then call Perspective.
    client = get_cloudwatch_client()
    try:
        client.get_metric_statistics(
            Namespace=namespace,
            MetricName=metric_name,
            StartTime=start_time,
            EndTime=end_time,
            Period=60,
            Statistics=["Average"]
        )
    except Exception as exc:
        raise RuntimeError(f"Failed to verify CloudWatch credentials: {exc}")
    # Simulate label list – in a real scenario you would parse DescribeAlarms output.
    # Here we mock a simple list of annotations.
    annotations = [
        "Critical service outage in production.",
        "User reported hate speech encountered.",
        "System recovered."
    ]
    # Call Perspective API
    perspective_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    perspective_key = os.getenv("PERSPECTIVE_API_KEY")
    if not perspective_key:
        raise RuntimeError("PERSPECTIVE_API_KEY not set")
    headers = {"Content-Type": "application/json"}
    results = []
    for txt in annotations:
        payload = {"comment": {"text": txt}, "languages": ["en"], "requestedAttributes": {"TOXICITY": {}}}
        resp = requests.post(perspective_url, json=payload, params={"key": perspective_key}, headers=headers)
        data = resp.json()
        score = data["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
        safe = score < 0.5
        results.append({"text": txt, "toxicity_score": score, "safe": safe})
    # Return simple safety report
    report = {
        "metric": {
            "namespace": namespace,
            "name": metric_name,
            "time_window": {
                "start": start_time,
                "end": end_time
            }
        },
        "annotation_safety": results
    }
    return report

if __name__ == "__main__":
    start = os.getenv("AWS_START_TIME", "2024-08-20T00:00:00Z")
    end = os.getenv("AWS_END_TIME", "2024-08-20T01:00:00Z")
    safe_report = check_annotations_safe(
        os.getenv("AWS_NAMESPACE", "AWS/MyService"),
        os.getenv("AWS_METRIC_NAME", "CustomMetric"),
        start,
        end
    )
    print(safe_report)
