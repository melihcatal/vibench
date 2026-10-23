import os
from datetime import datetime, timedelta
from typing import List, Dict

from datadog_api_client.v2.api import metrics_api
from datadog_api_client.v2.model.metrics_aggregator import MetricsAggregator
from datadog_api_client.v2.model.metrics_data_source import MetricsDataSource
from datadog_api_client.v2.model.metrics_query_request import MetricsQueryRequest
from datadog_api_client.v2.model.metrics_timeseries_query import MetricsTimeseriesQuery

from observability_client import ClientFactory
from observability_models import MetricStatistics, MetricStatistic


def get_datadog_aggregate_stats(
    metric_query: str, minutes_ago: int = 60, aggregators: List[str] = None
) -> List[MetricStatistics]:
    """
    Retrieves aggregated statistics for a Datadog metric over a time window.

    Args:
        metric_query: The Datadog metric query string (e.g., "system.cpu.idle{*}").
        minutes_ago: The number of minutes in the past to query.
        aggregators: A list of aggregators like "avg", "min", "max", "sum".

    Returns:
        A list of MetricStatistics objects.
    """
    if aggregators is None:
        aggregators = ["avg", "max", "min", "sum"]
    
    api_instance = ClientFactory.get_datadog_metrics_api()

    now = datetime.now()
    start_time = now - timedelta(minutes=minutes_ago)
    
    from_ts = int(start_time.timestamp())
    to_ts = int(now.timestamp())

    body = MetricsQueryRequest(
        data=MetricsTimeseriesQuery(
            queries=[
                {
                    "data_source": MetricsDataSource.METRICS,
                    "query": metric_query,
                    "name": "query1",
                }
            ],
            formulas=[{"formula": f"{agg}(query1)"} for agg in aggregators],
            _from=from_ts,
            to=to_ts,
        )
    )

    try:
        response = api_instance.query_timeseries_data(body=body)
        results = []
        if response.data and response.data.attributes and response.data.attributes.series:
            for series in response.data.attributes.series:
                stats = []
                # Assuming the last point is the aggregated value over the window
                if series.values and len(series.values) > 0:
                    for i, agg_formula in enumerate(response.data.attributes.formulas):
                        stat_name = agg_formula.get("formula", f"agg_{i}").split("(")[0]
                        # This example assumes a single value for the whole period.
                        # Datadog might return a series of aggregated values.
                        # We take the first non-None value if available.
                        agg_value = None
                        for val_tuple in series.values:
                            if len(val_tuple) > 1 and val_tuple[1] is not None:
                                agg_value = val_tuple[1]
                                break
                        if agg_value is not None:
                             stats.append(MetricStatistic(name=stat_name, value=agg_value))

                results.append(
                    MetricStatistics(
                        metric_name=series.metric,
                        statistics=stats,
                        dimensions=series.group_tags,
                    )
                )
        return results
    except Exception as e:
        print(f"Error calling Datadog API: {e}")
        return []

# Example usage would require Datadog API keys (DD_API_KEY, DD_APP_KEY) set as env vars.
# if __name__ == "__main__":
#     # Make sure DD_SITE is set, e.g., "datadoghq.com"
#     if os.environ.get("DD_API_KEY") and os.environ.get("DD_APP_KEY"):
#         stats = get_datadog_aggregate_stats("avg:system.cpu.idle{*}", minutes_ago=30)
#         for stat_set in stats:
#             print(f"Metric: {stat_set.metric_name}, Dimensions: {stat_set.dimensions}")
#             for stat in stat_set.statistics:
#                 print(f"  - {stat.name}: {stat.value}")
#     else:
#         print("DD_API_KEY and DD_APP_KEY environment variables must be set.")
