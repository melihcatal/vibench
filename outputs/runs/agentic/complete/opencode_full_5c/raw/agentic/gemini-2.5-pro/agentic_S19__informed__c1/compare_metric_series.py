import time
from typing import List, Dict, Tuple
from observability_client import get_datadog_client
from observability_models import MetricSeries, MetricDataPoint


def compare_metric_series(
    metric_name: str,
    dimensions1: Dict[str, str],
    dimensions2: Dict[str, str],
    hours: int = 1,
) -> Tuple[List[MetricSeries], List[MetricSeries]]:
    client = get_datadog_client()

    to_ts = int(time.time())
    from_ts = to_ts - (hours * 3600)

    dim_str1 = ",".join([f"{k}:{v}" for k, v in dimensions1.items()])
    query1 = f"avg:{metric_name}{{{dim_str1}}}"

    dim_str2 = ",".join([f"{k}:{v}" for k, v in dimensions2.items()])
    query2 = f"avg:{metric_name}{{{dim_str2}}}"

    combined_query = f"{query1},{query2}"

    try:
        data = client.query_metrics(combined_query, from_ts, to_ts)

        series1_list = []
        series2_list = []

        if data.get("status") == "ok":
            for series in data.get("series", []):
                points = [
                    MetricDataPoint(timestamp=int(p[0] / 1000), value=p[1])
                    for p in series.get("pointlist", [])
                    if p[1] is not None
                ]
                metric_series = MetricSeries(
                    metric_name=series.get("metric"),
                    points=points,
                    tags=series.get("tag_set"),
                )

                # Check if the series tags match the requested dimensions
                series_tags = set(series.get("tag_set", []))
                dim1_tags = set(f"{k}:{v}" for k, v in dimensions1.items())
                dim2_tags = set(f"{k}:{v}" for k, v in dimensions2.items())

                if dim1_tags.issubset(series_tags):
                    series1_list.append(metric_series)
                elif dim2_tags.issubset(series_tags):
                    series2_list.append(metric_series)

        return series1_list, series2_list

    except Exception as e:
        print(f"Error comparing metric series on Datadog: {e}")
        return [], []
