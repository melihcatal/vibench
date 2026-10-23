import os
from datetime import datetime, timedelta
import json
from local_helpers.observability_client import get_client
from local_helpers.observability_models import CompareRequest, CompareResult
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("METRICS_PROVIDER", "AZURE_MONITOR")  # default provider

# Dummy utility to fetch recent metric data for summarization
# In a real system this would orchestrate calls to the selected provider's SDK client


def fetch_recent_series(provider, resource_id, metric_name, window_hours=24):
    client = get_client(provider)
    now = datetime.utcnow()
    start = now - timedelta(hours=window_hours)
    end = now
    if provider == "AZURE_MONITOR":
        # Azure: compare two identical series to get data
        req = CompareRequest(
            series=[
                {
                    "resource_id": resource_id,
                    "metric_name": metric_name,
                    "filter": None,
                    "start_time": start,
                    "end_time": end,
                },
                {
                    "resource_id": resource_id,
                    "metric_name": metric_name,
                    "filter": None,
                    "start_time": start,
                    "end_time": end,
                },
            ]
        )
        result = client.compare_metric_series(
            resource_id, metric_name, None, resource_id, None, start, end
        )
        # Azure returns CompareResult; extract first series datapoints
        return result.series[0].datapoints
    elif provider == "CLOUDWATCH":
        # AWS placeholder (similar logic)
        pass
    else:
        raise NotImplementedError(f"fetch_recent_series not implemented for {provider}")


def summarize_metric(resource_id, metric_name, window_hours=24):
    series = fetch_recent_series(PROVIDER, resource_id, metric_name, window_hours)
    if not series:
        return {"summary": f"No data found for {resource_id}.{metric_name}"}
    # Compute simple summary: min, max, avg, total, count
    values = [pt["value"] for pt in series if pt.get("value") is not None]
    summary = {}
    if values:
        summary["min"] = min(values)
        summary["max"] = max(values)
        summary["avg"] = sum(values) / len(values)
        summary["total"] = sum(values)
        summary["count"] = len(values)
    else:
        summary = {"min": None, "max": None, "avg": None, "total": None, "count": 0}
    summary["resource"] = resource_id
    summary["metric"] = metric_name
    summary["window_hours"] = window_hours
    return {"summary": summary}


if __name__ == "__main__":
    # Example usage (remove when integrating into larger pipeline)
    print(json.dumps(summarize_metric("my-resource-id", "cpuUsage", 24), indent=2))
