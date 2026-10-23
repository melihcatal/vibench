from datetime import timedelta

from observability_client import cloudwatch_client, load_config
from observability_models import MetricComparisonRequest, normalize_dimensions, utc_now


def _fetch(
    metric_name, namespace, start_time, end_time, period, statistics, dimensions
):
    resp = cloudwatch_client().get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=list(statistics),
        Dimensions=normalize_dimensions(dimensions),
    )
    return resp.get("Datapoints", [])


def compare_metric_series(
    metric_name=None,
    namespace=None,
    minutes=60,
    period=300,
    left_dimensions=None,
    right_dimensions=None,
):
    cfg = load_config()
    req = MetricComparisonRequest(
        metric_name=metric_name or cfg.metric_name,
        namespace=namespace or cfg.namespace,
        start_time=utc_now() - timedelta(minutes=minutes),
        end_time=utc_now(),
        period=period,
        left_dimensions=left_dimensions,
        right_dimensions=right_dimensions,
    )
    return {
        "left": _fetch(
            req.metric_name,
            req.namespace,
            req.start_time,
            req.end_time,
            req.period,
            req.statistics,
            req.left_dimensions,
        ),
        "right": _fetch(
            req.metric_name,
            req.namespace,
            req.start_time,
            req.end_time,
            req.period,
            req.statistics,
            req.right_dimensions,
        ),
    }
