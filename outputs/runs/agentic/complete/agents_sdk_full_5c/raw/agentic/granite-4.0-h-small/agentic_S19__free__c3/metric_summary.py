import os
from observability_client import get_client
from observability_models import TimeInterval, MetricQueryResponse

# ----------- LATER-STEP IMPLEMENTATION ------------
# GCP Monitoring (managed metrics) via monitoring.googleapis.com
# Provider signal: imported client from google.api_core.monitored_resource

def metric_summary(metric_type: str, time_window: TimeInterval) -> Dict[str, Any]:
    """Summarize recent metric trends or anomalies using GCP Monitoring data.

    Args:
        metric_type: Metric descriptor name.
        time_window: NamedTuple with start_time and end_time strings.

    Returns:
        Dictionary containing summary stats (count, mean, min, max, recent delta). Includes a provider marker.
    """
    client = get_client()
    end_time = time_window.end_time
    start_time = time_window.start_time
    request = {
        'name': f"projects/{os.getenv('GCP_PROJECT')}/metricDescriptors/{metric_type}",
        'interval': {'startTime': start_time, 'endTime': end_time},
        'aggregation': {'alignmentPeriod': '60s', 'perSeriesAligner': 'ALIGN_MEAN'}
    }
    response = client.query_time_series(request)
    # extract simple stats
    points = []
    for ts in response.time_series:
        points.extend(ts.points)
    if not points:
        return {'metric': metric_type, 'summary': None, 'provider': 'GCP_MONITORING'}
    values = [p.value.double_value for p in points if p.value.WhichOneof('value_type') == 'double_value']
    summary = {
        'count': len(values),
        'mean': sum(values) / len(values) if values else None,
        'min': min(values) if values else None,
        'max': max(values) if values else None,
        'provider': 'GCP_MONITORING',
        'window': str(time_window)
    }
    return summary
