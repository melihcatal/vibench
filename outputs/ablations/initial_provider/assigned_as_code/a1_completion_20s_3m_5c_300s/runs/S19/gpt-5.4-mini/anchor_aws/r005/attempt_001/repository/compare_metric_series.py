from observability_client import cloudwatch_client
from observability_models import build_dimensions, normalize_datapoints, to_utc_datetime


def _series(client, namespace, metric, dimensions, start_time, end_time, period_seconds):
    response = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric,
        Dimensions=build_dimensions(dimensions),
        StartTime=to_utc_datetime(start_time),
        EndTime=to_utc_datetime(end_time),
        Period=period_seconds,
        Statistics=["Average"],
    )
    return normalize_datapoints(response.get("Datapoints", []), "Average")


def compare_metric_series(payload, config=None):
    config = config or {}
    client = cloudwatch_client(config)
    first = _series(
        client,
        config["namespace"],
        payload["metric"],
        payload.get("first_dimensions", config.get("first_dimensions", {})),
        payload["start_time"],
        payload["end_time"],
        config.get("period_seconds", 60),
    )
    second = _series(
        client,
        config["namespace"],
        payload["metric"],
        payload.get("second_dimensions", config.get("second_dimensions", {})),
        payload["start_time"],
        payload["end_time"],
        config.get("period_seconds", 60),
    )
    return {"first": first, "second": second}
