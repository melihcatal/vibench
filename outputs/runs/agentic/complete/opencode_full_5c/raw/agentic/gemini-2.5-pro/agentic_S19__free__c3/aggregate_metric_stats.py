import time
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_monitoring_client, get_project_id
from observability_models import AggregatedMetricData


def get_aggregated_metric(
    metric_name: str, minutes: int = 60, aggregation_type: str = "ALIGN_MEAN"
) -> AggregatedMetricData:
    client = get_monitoring_client()
    project_id = get_project_id()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": Timestamp(seconds=seconds, nanos=nanos),
            "start_time": Timestamp(seconds=seconds - (minutes * 60), nanos=nanos),
        }
    )

    aggregation_map = {
        "ALIGN_NONE": monitoring_v3.Aggregation.Aligner.ALIGN_NONE,
        "ALIGN_DELTA": monitoring_v3.Aggregation.Aligner.ALIGN_DELTA,
        "ALIGN_RATE": monitoring_v3.Aggregation.Aligner.ALIGN_RATE,
        "ALIGN_INTERPOLATE": monitoring_v3.Aggregation.Aligner.ALIGN_INTERPOLATE,
        "ALIGN_NEXT_OLDER": monitoring_v3.Aggregation.Aligner.ALIGN_NEXT_OLDER,
        "ALIGN_MIN": monitoring_v3.Aggregation.Aligner.ALIGN_MIN,
        "ALIGN_MAX": monitoring_v3.Aggregation.Aligner.ALIGN_MAX,
        "ALIGN_MEAN": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        "ALIGN_COUNT": monitoring_v3.Aggregation.Aligner.ALIGN_COUNT,
        "ALIGN_SUM": monitoring_v3.Aggregation.Aligner.ALIGN_SUM,
        "ALIGN_STDDEV": monitoring_v3.Aggregation.Aligner.ALIGN_STDDEV,
        "ALIGN_COUNT_TRUE": monitoring_v3.Aggregation.Aligner.ALIGN_COUNT_TRUE,
        "ALIGN_COUNT_FALSE": monitoring_v3.Aggregation.Aligner.ALIGN_COUNT_FALSE,
        "ALIGN_FRACTION_TRUE": monitoring_v3.Aggregation.Aligner.ALIGN_FRACTION_TRUE,
        "ALIGN_PERCENTILE_99": monitoring_v3.Aggregation.Aligner.ALIGN_PERCENTILE_99,
        "ALIGN_PERCENTILE_95": monitoring_v3.Aggregation.Aligner.ALIGN_PERCENTILE_95,
        "ALIGN_PERCENTILE_50": monitoring_v3.Aggregation.Aligner.ALIGN_PERCENTILE_50,
        "ALIGN_PERCENTILE_05": monitoring_v3.Aggregation.Aligner.ALIGN_PERCENTILE_05,
        "ALIGN_PERCENT_CHANGE": monitoring_v3.Aggregation.Aligner.ALIGN_PERCENT_CHANGE,
    }

    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": minutes * 60},
            "per_series_aligner": aggregation_map.get(aggregation_type, "ALIGN_MEAN"),
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_name}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    value = 0.0
    # Assuming we get one point for the whole interval due to aggregation
    for result in results:
        if result.points:
            value = result.points[0].value.double_value
            break

    return AggregatedMetricData(
        metric_name=metric_name, aggregation=aggregation_type, value=value
    )
